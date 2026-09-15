"""Opt-in adapter for Hindsight's public retain and recall API."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Any, Callable

from chronicle_bench.providers.base import BenchmarkAdapter, ProviderError


HttpCallable = Callable[[str, str, dict[str, Any], dict[str, str]], Any]


class HindsightAdapter(BenchmarkAdapter):
    name = "hindsight"
    version = "0.1.0"
    capabilities = frozenset({"retain", "recall"})

    def __init__(
        self,
        *,
        base_url: str,
        bank_id: str,
        api_token: str | None = None,
        http: HttpCallable | None = None,
    ) -> None:
        if not base_url or not bank_id:
            raise ValueError("Hindsight base URL and disposable bank ID are required")
        self.base_url = base_url.rstrip("/")
        self.bank_id = bank_id
        self.api_token = api_token
        self.http = http or self._request
        self.case_id = ""

    @classmethod
    def from_environment(cls) -> "HindsightAdapter":
        return cls(
            base_url=os.environ.get("HINDSIGHT_BASE_URL")
            or os.environ.get("HINDSIGHT_API_URL", ""),
            bank_id=os.environ.get("HINDSIGHT_BANK_ID", ""),
            api_token=os.environ.get("HINDSIGHT_API_TOKEN"),
        )

    def reset(self, case_id: str) -> None:
        # A unique document ID is used per case. The adapter never deletes a bank.
        self.case_id = case_id

    def configuration(self) -> dict[str, str]:
        return {"base_url": self.base_url, "bank_id": self.bank_id}

    def execute(self, operation: dict[str, Any]) -> dict[str, Any]:
        kind = operation["op"]
        if kind == "retain":
            return self._retain(operation)
        if kind == "recall":
            return self._recall(operation)
        raise ProviderError(f"Hindsight adapter does not support {kind}")

    def _retain(self, operation: dict[str, Any]) -> dict[str, Any]:
        record = operation["record"]
        item: dict[str, Any] = {
            "content": record["text"],
            "context": f"Chronicle benchmark case {self.case_id}",
            "document_id": f"chronicle-bench:{self.case_id}:{record['id']}",
            "metadata": {
                "chronicle_fixture_id": record["id"],
                "chronicle_scope": record["scope"],
            },
        }
        if record.get("valid_from"):
            item["timestamp"] = record["valid_from"]
        if record.get("tags"):
            item["tags"] = record["tags"]
        response = self._call(
            "POST",
            f"/v1/default/banks/{self.bank_id}/memories",
            {"items": [item]},
        )
        return {"accepted": True, "id": record["id"], "provider_response": bool(response)}

    def _recall(self, operation: dict[str, Any]) -> dict[str, Any]:
        query = operation["query"]
        body: dict[str, Any] = {
            "query": query["text"],
            "max_tokens": int(query.get("max_context_tokens", 4096)),
        }
        if query.get("tags"):
            body["tags"] = query["tags"]
            # Strict matching prevents unrelated or untagged bank contents from
            # contaminating a benchmark case.
            body["tags_match"] = query.get("tags_match", "all_strict")
        response = self._call(
            "POST",
            f"/v1/default/banks/{self.bank_id}/memories/recall",
            body,
        )
        raw_items = self._extract_items(response)
        items: list[dict[str, Any]] = []
        for raw in raw_items[: int(query.get("k", 5))]:
            metadata = raw.get("metadata") or {}
            document_id = str(raw.get("document_id") or "")
            fixture_id = metadata.get("chronicle_fixture_id")
            if not fixture_id and document_id.startswith(f"chronicle-bench:{self.case_id}:"):
                fixture_id = document_id.rsplit(":", 1)[-1]
            fixture_id = fixture_id or raw.get("memory_id") or raw.get("id")
            text = raw.get("text") or raw.get("content") or raw.get("memory") or ""
            provenance = raw.get("provenance") or raw.get("sources") or []
            items.append(
                {
                    "id": str(fixture_id),
                    "text": str(text),
                    "score": float(raw.get("score") or raw.get("relevance") or 0.0),
                    "provenance": provenance,
                    "context_tokens": max(1, (len(str(text)) + 3) // 4),
                }
            )
        return {
            "items": items,
            "context_tokens": sum(int(item["context_tokens"]) for item in items),
        }

    @staticmethod
    def _extract_items(response: Any) -> list[dict[str, Any]]:
        if isinstance(response, list):
            return [item for item in response if isinstance(item, dict)]
        if not isinstance(response, dict):
            raise ProviderError("unexpected Hindsight response type")
        for key in ("results", "memories", "items"):
            value = response.get(key)
            if isinstance(value, list):
                return [item for item in value if isinstance(item, dict)]
        data = response.get("data")
        if isinstance(data, dict):
            return HindsightAdapter._extract_items(data)
        return []

    def _call(self, method: str, path: str, body: dict[str, Any]) -> Any:
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        if self.api_token:
            headers["Authorization"] = f"Bearer {self.api_token}"
        try:
            return self.http(method, f"{self.base_url}{path}", body, headers)
        except ProviderError:
            raise
        except Exception as exc:
            raise ProviderError(f"Hindsight request failed: {exc}") from exc

    @staticmethod
    def _request(
        method: str, url: str, body: dict[str, Any], headers: dict[str, str]
    ) -> Any:
        request = urllib.request.Request(
            url,
            data=json.dumps(body).encode("utf-8"),
            headers=headers,
            method=method,
        )
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                payload = response.read()
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")[:500]
            raise ProviderError(f"Hindsight HTTP {exc.code}: {detail}") from exc
        except urllib.error.URLError as exc:
            raise ProviderError(f"Hindsight connection failed: {exc.reason}") from exc
        if not payload:
            return {}
        return json.loads(payload.decode("utf-8"))
