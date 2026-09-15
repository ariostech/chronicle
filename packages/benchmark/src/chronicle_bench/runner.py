"""Suite loading, execution, scoring, and result recording."""

from __future__ import annotations

import hashlib
import json
import os
import platform
import random
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path
from statistics import fmean
from typing import Any

from chronicle_bench.metrics import (
    ndcg_at_k,
    percentile,
    precision_at_k,
    recall_at_k,
    reciprocal_rank,
)
from chronicle_bench.providers.base import BenchmarkAdapter, OperationRejected, ProviderError


class SuiteError(ValueError):
    """The suite or result contract is invalid."""


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _git_metadata(root: Path) -> tuple[str, bool]:
    try:
        revision = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=root,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        dirty = bool(
            subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=root,
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()
        )
        return revision, dirty
    except (OSError, subprocess.CalledProcessError):
        return "unknown", True


def load_suite(path: Path) -> tuple[dict[str, Any], str]:
    raw = path.read_bytes()
    try:
        suite = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise SuiteError(f"invalid suite JSON: {exc}") from exc
    validate_suite(suite)
    return suite, _sha256(raw)


def validate_suite(suite: Any) -> None:
    if not isinstance(suite, dict):
        raise SuiteError("suite must be a JSON object")
    required = {
        "schema_version": str,
        "suite_id": str,
        "dataset_version": str,
        "description": str,
        "profile": str,
        "default_k": int,
        "cases": list,
    }
    for field, expected_type in required.items():
        if field not in suite or not isinstance(suite[field], expected_type):
            raise SuiteError(f"suite field {field!r} must be {expected_type.__name__}")
    if suite["schema_version"] != "0.1":
        raise SuiteError(f"unsupported schema version: {suite['schema_version']}")
    if suite["profile"] not in {"contract", "provider-retrieval", "chronicle-gateway"}:
        raise SuiteError(f"unknown profile: {suite['profile']}")
    seen: set[str] = set()
    known_operations = {
        "retain",
        "recall",
        "supersede",
        "delete",
        "authorize",
        "promote",
        "fail_next",
    }
    for case in suite["cases"]:
        if not isinstance(case, dict):
            raise SuiteError("every case must be an object")
        for field in ("id", "category", "description", "required_capabilities", "operations"):
            if field not in case:
                raise SuiteError(f"case is missing {field}")
        case_id = case["id"]
        if not isinstance(case_id, str) or not case_id:
            raise SuiteError("case id must be a non-empty string")
        if case_id in seen:
            raise SuiteError(f"duplicate case id: {case_id}")
        seen.add(case_id)
        if not isinstance(case["required_capabilities"], list):
            raise SuiteError(f"case {case_id} required_capabilities must be a list")
        if not isinstance(case["operations"], list) or not case["operations"]:
            raise SuiteError(f"case {case_id} must contain operations")
        for operation in case["operations"]:
            if not isinstance(operation, dict) or operation.get("op") not in known_operations:
                raise SuiteError(f"case {case_id} contains an invalid operation")


def validate_result(result: Any) -> None:
    if not isinstance(result, dict):
        raise SuiteError("result must be an object")
    required = {
        "schema_version",
        "suite",
        "subject",
        "environment",
        "started_at",
        "completed_at",
        "seed",
        "cases",
        "aggregates",
        "disqualifying_failures",
        "conformant",
        "outcome_digest",
    }
    missing = sorted(required - result.keys())
    if missing:
        raise SuiteError(f"result is missing: {', '.join(missing)}")
    if result["schema_version"] != "0.1":
        raise SuiteError("unsupported result schema version")
    if not isinstance(result["cases"], list):
        raise SuiteError("result cases must be a list")
    if not isinstance(result["conformant"], bool):
        raise SuiteError("result conformant must be boolean")
    digest = result["outcome_digest"]
    if not isinstance(digest, str) or len(digest) != 64:
        raise SuiteError("result outcome_digest must be a SHA-256 hex string")


def _assert_operation(
    operation: dict[str, Any],
    response: dict[str, Any],
) -> tuple[list[str], dict[str, float]]:
    failures: list[str] = []
    metrics: dict[str, float] = {}
    kind = operation["op"]
    expected_state = operation.get("expect")
    if expected_state in {"rejected", "denied"}:
        failures.append(f"{kind} unexpectedly succeeded")
        return failures, metrics
    if kind == "authorize" and expected_state:
        actual = "allow" if response.get("allowed") else "deny"
        if actual != expected_state:
            failures.append(f"authorization expected {expected_state}, got {actual}")
    if kind != "recall":
        return failures, metrics

    expected = operation.get("expected", {})
    items = response.get("items", [])
    ranked_ids = [str(item.get("id")) for item in items]
    relevant_ids = set(expected.get("relevant_ids", []))
    forbidden_ids = set(expected.get("forbidden_ids", []))
    k = int(operation["query"].get("k", len(ranked_ids) or 1))
    metrics = {
        "precision_at_k": precision_at_k(ranked_ids, relevant_ids, k),
        "recall_at_k": recall_at_k(ranked_ids, relevant_ids, k),
        "mrr": reciprocal_rank(ranked_ids, relevant_ids, k),
        "ndcg_at_k": ndcg_at_k(ranked_ids, relevant_ids, k),
        "policy_violations": float(len(set(ranked_ids) & forbidden_ids)),
        "context_tokens": float(response.get("context_tokens", 0)),
    }
    if metrics["policy_violations"]:
        leaked = sorted(set(ranked_ids) & forbidden_ids)
        failures.append(f"forbidden results returned: {', '.join(leaked)}")

    if expected.get("require_provenance"):
        with_provenance = sum(bool(item.get("provenance")) for item in items)
        completeness = with_provenance / len(items) if items else (1.0 if not relevant_ids else 0.0)
        metrics["provenance_completeness"] = completeness
    required_trust = expected.get("required_trust")
    if required_trust:
        mismatched = [
            str(item.get("id"))
            for item in items
            if item.get("trust") != required_trust
        ]
        if mismatched:
            failures.append(
                f"results have unexpected trust classification: {', '.join(mismatched)}"
            )
    required_authority = expected.get("required_authority")
    if required_authority:
        mismatched = [
            str(item.get("id"))
            for item in items
            if item.get("authority") != required_authority
        ]
        if mismatched:
            failures.append(
                f"results have unexpected authority: {', '.join(mismatched)}"
            )
    budget = expected.get("max_context_tokens")
    if budget is not None and metrics["context_tokens"] > float(budget):
        failures.append(
            f"context budget exceeded: {metrics['context_tokens']:.0f} > {int(budget)}"
        )
    for metric, minimum in expected.get("minimum", {}).items():
        actual = metrics.get(metric)
        if actual is None:
            failures.append(f"required metric missing: {metric}")
        elif actual < float(minimum):
            failures.append(f"{metric} {actual:.4f} is below {float(minimum):.4f}")
    return failures, metrics


def _case_metrics(operation_metrics: list[dict[str, float]]) -> dict[str, float]:
    names = sorted({name for item in operation_metrics for name in item if name != "latency_ms"})
    aggregated: dict[str, float] = {}
    for name in names:
        values = [item[name] for item in operation_metrics if name in item]
        aggregated[name] = round(fmean(values), 6)
    return aggregated


def run_suite(
    suite: dict[str, Any],
    suite_sha256: str,
    adapter: BenchmarkAdapter,
    *,
    seed: int = 0,
    source_root: Path | None = None,
    subject_version: str | None = None,
    model_id: str = "none",
    configuration_label: str = "default",
) -> dict[str, Any]:
    validate_suite(suite)
    random.seed(seed)
    started_at = _now()
    source_root = source_root or Path.cwd()
    revision, dirty = _git_metadata(source_root)
    case_results: list[dict[str, Any]] = []
    disqualifying: list[str] = []
    required_skips: list[str] = []
    all_latencies: list[float] = []

    for case in suite["cases"]:
        case_id = case["id"]
        missing = sorted(set(case["required_capabilities"]) - adapter.capabilities)
        if missing:
            required = bool(case.get("required", True))
            case_results.append(
                {
                    "id": case_id,
                    "category": case["category"],
                    "security_gate": bool(case.get("security_gate", False)),
                    "status": "skipped",
                    "reason": f"adapter lacks: {', '.join(missing)}",
                    "failures": [],
                    "metrics": {},
                    "operations": [],
                }
            )
            if required:
                required_skips.append(case_id)
            continue

        adapter.reset(case_id)
        failures: list[str] = []
        operation_results: list[dict[str, Any]] = []
        measured: list[dict[str, float]] = []

        for index, operation in enumerate(case["operations"]):
            operation_name = operation["op"]
            began = time.perf_counter()
            try:
                response = adapter.execute(operation)
                latency_ms = (time.perf_counter() - began) * 1000.0
                all_latencies.append(latency_ms)
                if operation.get("expected_error"):
                    op_failures = [f"{operation_name} unexpectedly succeeded"]
                    op_metrics: dict[str, float] = {}
                else:
                    op_failures, op_metrics = _assert_operation(operation, response)
                op_metrics["latency_ms"] = round(latency_ms, 6)
                measured.append(op_metrics)
                failures.extend(f"operation {index + 1}: {item}" for item in op_failures)
                operation_results.append(
                    {
                        "op": operation_name,
                        "status": "passed" if not op_failures else "failed",
                        "metrics": op_metrics,
                        "failures": op_failures,
                    }
                )
            except (OperationRejected, ProviderError) as exc:
                latency_ms = (time.perf_counter() - began) * 1000.0
                all_latencies.append(latency_ms)
                expected_rejection = operation.get("expect") in {"rejected", "denied"}
                expected_error = bool(operation.get("expected_error"))
                passed = expected_rejection or expected_error
                if not passed:
                    failures.append(f"operation {index + 1}: {exc}")
                operation_results.append(
                    {
                        "op": operation_name,
                        "status": "passed" if passed else "failed",
                        "error_type": type(exc).__name__,
                        "metrics": {"latency_ms": round(latency_ms, 6)},
                        "failures": [] if passed else [str(exc)],
                    }
                )

        status = "passed" if not failures else "failed"
        security_gate = bool(case.get("security_gate", False))
        if security_gate and failures:
            disqualifying.append(case_id)
        case_results.append(
            {
                "id": case_id,
                "category": case["category"],
                "security_gate": security_gate,
                "status": status,
                "failures": failures,
                "metrics": _case_metrics(measured),
                "operations": operation_results,
            }
        )

    passed = sum(case["status"] == "passed" for case in case_results)
    failed = sum(case["status"] == "failed" for case in case_results)
    skipped = sum(case["status"] == "skipped" for case in case_results)
    metric_names = sorted(
        {
            name
            for case in case_results
            for name in case.get("metrics", {})
            if name not in {"latency_ms"}
        }
    )
    means = {
        name: round(
            fmean(
                case["metrics"][name]
                for case in case_results
                if name in case.get("metrics", {})
            ),
            6,
        )
        for name in metric_names
    }
    configuration = adapter.configuration()
    result: dict[str, Any] = {
        "schema_version": "0.1",
        "suite": {
            "id": suite["suite_id"],
            "dataset_version": suite["dataset_version"],
            "profile": suite["profile"],
            "sha256": suite_sha256,
        },
        "subject": {
            "adapter": adapter.name,
            "adapter_version": adapter.version,
            "provider_version": subject_version or "unspecified",
            "model_id": model_id,
            "configuration_label": configuration_label,
            "configuration_fingerprint": _sha256(_canonical(configuration)),
        },
        "environment": {
            "python": platform.python_version(),
            "implementation": platform.python_implementation(),
            "operating_system": platform.system(),
            "release": platform.release(),
            "architecture": platform.machine(),
            "source_revision": revision,
            "dirty_worktree": dirty,
        },
        "started_at": started_at,
        "completed_at": _now(),
        "seed": seed,
        "cases": case_results,
        "aggregates": {
            "case_count": len(case_results),
            "passed": passed,
            "failed": failed,
            "skipped": skipped,
            "mean_metrics": means,
            "latency_ms": {
                "p50": round(percentile(all_latencies, 50), 6),
                "p95": round(percentile(all_latencies, 95), 6),
            },
        },
        "required_skips": required_skips,
        "disqualifying_failures": disqualifying,
        "conformant": failed == 0 and not required_skips and not disqualifying,
    }
    stable_outcome = {
        "suite": result["suite"],
        "subject": {
            "adapter": result["subject"]["adapter"],
            "adapter_version": result["subject"]["adapter_version"],
        },
        "cases": [
            {
                "id": case["id"],
                "status": case["status"],
                "failures": case.get("failures", []),
                "metrics": case.get("metrics", {}),
            }
            for case in case_results
        ],
        "required_skips": required_skips,
        "disqualifying_failures": disqualifying,
        "conformant": result["conformant"],
    }
    result["outcome_digest"] = _sha256(_canonical(stable_outcome))
    validate_result(result)
    return result


def write_result(path: Path, result: dict[str, Any]) -> None:
    validate_result(result)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(temporary, path)
