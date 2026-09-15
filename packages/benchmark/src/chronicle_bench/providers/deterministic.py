"""Deterministic reference semantics for Chronicle contract fixtures."""

from __future__ import annotations

import re
from copy import deepcopy
from datetime import datetime, timezone
from typing import Any

from chronicle_bench.providers.base import (
    BenchmarkAdapter,
    OperationRejected,
    ProviderError,
)


TOKEN = re.compile(r"[a-z0-9]+")
SYNTHETIC_SECRET = re.compile(r"\bchr_test_secret_[A-Za-z0-9_-]{8,}\b")
STOPWORDS = {
    "a",
    "an",
    "and",
    "does",
    "do",
    "how",
    "is",
    "of",
    "the",
    "to",
    "use",
    "uses",
    "what",
    "which",
    "who",
}
AUTHORITY_WEIGHT = {
    "untrusted": 0,
    "memory": 1,
    "candidate": 2,
    "reviewed": 3,
    "approved": 4,
}


def _parse_time(value: str | None) -> datetime:
    if value is None:
        return datetime.now(timezone.utc)
    normalized = value.replace("Z", "+00:00")
    parsed = datetime.fromisoformat(normalized)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _tokens(value: str) -> set[str]:
    return {token for token in TOKEN.findall(value.lower()) if token not in STOPWORDS}


def _scope_allowed(scope: str, allowed: list[str]) -> bool:
    for pattern in allowed:
        if pattern == "*" or pattern == scope:
            return True
        if pattern.endswith("/*") and scope.startswith(pattern[:-1]):
            return True
    return False


class DeterministicAdapter(BenchmarkAdapter):
    """A small oracle for runner and Chronicle semantic contract tests.

    This is intentionally not a production retrieval implementation or baseline.
    """

    name = "deterministic-contract"
    version = "0.1.0"
    capabilities = frozenset(
        {
            "retain",
            "recall",
            "supersede",
            "delete",
            "authorize",
            "promote",
            "simulate_outage",
        }
    )

    def __init__(self, *, leak_scopes: bool = False) -> None:
        self.leak_scopes = leak_scopes
        self.records: dict[str, dict[str, Any]] = {}
        self.fail_next_operation = False
        self.case_id = ""

    def reset(self, case_id: str) -> None:
        self.records = {}
        self.fail_next_operation = False
        self.case_id = case_id

    def configuration(self) -> dict[str, str]:
        return {"leak_scopes": str(self.leak_scopes).lower()}

    def execute(self, operation: dict[str, Any]) -> dict[str, Any]:
        kind = operation["op"]
        if kind == "fail_next":
            self.fail_next_operation = True
            return {"accepted": True}

        if self.fail_next_operation:
            self.fail_next_operation = False
            raise ProviderError("injected provider outage")

        handler = getattr(self, f"_execute_{kind}", None)
        if handler is None:
            raise ProviderError(f"unsupported operation: {kind}")
        return handler(operation)

    def _execute_retain(self, operation: dict[str, Any]) -> dict[str, Any]:
        record = deepcopy(operation["record"])
        record_id = record["id"]
        if record_id in self.records:
            raise OperationRejected(f"duplicate record id: {record_id}")
        if SYNTHETIC_SECRET.search(record["text"]):
            raise OperationRejected("synthetic secret rejected by capture screening")

        actor = operation.get("actor")
        if actor and not self._is_authorized(actor, "write", record["scope"]):
            raise OperationRejected("write is outside the principal's effective scope")

        record.setdefault("state", "active")
        record.setdefault("authority", "memory")
        record.setdefault("provenance", [])
        record.setdefault("tags", [])
        record.setdefault("aliases", [])
        self.records[record_id] = record
        return {"accepted": True, "id": record_id}

    def _execute_recall(self, operation: dict[str, Any]) -> dict[str, Any]:
        query = operation["query"]
        query_tokens = _tokens(query["text"])
        at = _parse_time(query.get("at"))
        principal = query.get("principal", {})
        requested_scopes = query.get("allowed_scopes", ["*"])
        principal_scopes = principal.get("allowed_read_scopes", ["*"])
        include_states = set(query.get("states", ["active", "stable"]))
        include_stale = bool(query.get("include_stale", False))

        ranked: list[tuple[float, str, dict[str, Any]]] = []
        for record_id, record in self.records.items():
            if not self._visible_at(record, at, include_states, include_stale):
                continue
            if not self.leak_scopes:
                if not _scope_allowed(record["scope"], requested_scopes):
                    continue
                if not _scope_allowed(record["scope"], principal_scopes):
                    continue

            searchable = " ".join(
                [record["text"], *record.get("tags", []), *record.get("aliases", [])]
            )
            overlap = len(query_tokens & _tokens(searchable))
            if query_tokens and overlap == 0:
                continue
            lexical = overlap / max(len(query_tokens), 1)
            authority = AUTHORITY_WEIGHT.get(record.get("authority", "untrusted"), 0)
            score = lexical + authority * 0.001
            ranked.append((score, record_id, record))

        ranked.sort(key=lambda item: (-item[0], item[1]))
        k = int(query.get("k", 5))
        budget = query.get("max_context_tokens")
        items: list[dict[str, Any]] = []
        token_total = 0
        for score, record_id, record in ranked:
            token_estimate = max(1, (len(record["text"]) + 3) // 4)
            if budget is not None and token_total + token_estimate > int(budget):
                continue
            items.append(
                {
                    "id": record_id,
                    "text": record["text"],
                    "score": round(score, 6),
                    "scope": record["scope"],
                    "state": record.get("state", "active"),
                    "authority": record.get("authority", "untrusted"),
                    "provenance": deepcopy(record.get("provenance", [])),
                    "trust": record.get("trust", "untrusted-data"),
                    "context_tokens": token_estimate,
                }
            )
            token_total += token_estimate
            if len(items) >= k:
                break

        return {"items": items, "context_tokens": token_total}

    def _execute_supersede(self, operation: dict[str, Any]) -> dict[str, Any]:
        old_id = operation["old_id"]
        new_id = operation["new_id"]
        if old_id not in self.records or new_id not in self.records:
            raise OperationRejected("both superseded and replacement records must exist")
        old = self.records[old_id]
        replacement = self.records[new_id]
        old["state"] = "superseded"
        old["superseded_by"] = new_id
        old["valid_to"] = replacement.get("valid_from", operation.get("at"))
        return {"accepted": True}

    def _execute_delete(self, operation: dict[str, Any]) -> dict[str, Any]:
        record_id = operation["id"]
        if record_id not in self.records:
            raise OperationRejected(f"unknown record id: {record_id}")
        self.records[record_id]["state"] = "deleted"
        self.records[record_id]["deleted_at"] = operation.get("at")
        return {"accepted": True}

    def _execute_authorize(self, operation: dict[str, Any]) -> dict[str, Any]:
        allowed = self._is_authorized(
            operation["principal"], operation["action"], operation["scope"]
        )
        return {"allowed": allowed}

    def _execute_promote(self, operation: dict[str, Any]) -> dict[str, Any]:
        record_id = operation["id"]
        record = self.records.get(record_id)
        if not record or record.get("state") != "candidate":
            raise OperationRejected("only candidate knowledge can be promoted")
        actor = operation["actor"]
        verifier = operation.get("verifier")
        if not verifier or verifier.get("id") == actor.get("id"):
            raise OperationRejected("promotion requires an independent verifier")
        if "knowledge_approver" not in verifier.get("roles", []):
            raise OperationRejected("verifier lacks the knowledge_approver role")
        if not self._is_authorized(verifier, "write", record["scope"]):
            raise OperationRejected("verifier cannot write the candidate scope")
        record["state"] = "stable"
        record["authority"] = "approved"
        record["verified_by"] = verifier["id"]
        return {"accepted": True}

    @staticmethod
    def _is_authorized(principal: dict[str, Any], action: str, scope: str) -> bool:
        key = "allowed_read_scopes" if action == "read" else "allowed_write_scopes"
        return _scope_allowed(scope, principal.get(key, []))

    @staticmethod
    def _visible_at(
        record: dict[str, Any],
        at: datetime,
        include_states: set[str],
        include_stale: bool,
    ) -> bool:
        state = record.get("state", "active")
        if state == "deleted":
            return False
        valid_from = record.get("valid_from")
        valid_to = record.get("valid_to")
        if valid_from and at < _parse_time(valid_from):
            return False
        if valid_to and at >= _parse_time(valid_to):
            return False
        if state == "superseded":
            if not valid_to or at >= _parse_time(valid_to):
                return False
        elif state not in include_states:
            return False
        stale_after = record.get("stale_after")
        if stale_after and at >= _parse_time(stale_after) and not include_stale:
            return False
        return True
