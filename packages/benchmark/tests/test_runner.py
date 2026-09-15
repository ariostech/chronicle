import json
import tempfile
import unittest
from pathlib import Path

from chronicle_bench.providers.deterministic import DeterministicAdapter
from chronicle_bench.runner import (
    SuiteError,
    load_suite,
    run_suite,
    validate_result,
    write_result,
)


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
CONTRACT_SUITE = PACKAGE_ROOT / "fixtures" / "v0.1" / "contract.json"


class RunnerTests(unittest.TestCase):
    def test_contract_suite_conforms(self) -> None:
        suite, digest = load_suite(CONTRACT_SUITE)
        result = run_suite(suite, digest, DeterministicAdapter(), source_root=PACKAGE_ROOT)
        validate_result(result)
        self.assertTrue(result["conformant"])
        self.assertEqual(result["aggregates"]["failed"], 0)
        self.assertEqual(result["aggregates"]["skipped"], 0)
        self.assertEqual(result["disqualifying_failures"], [])

    def test_outcome_digest_is_deterministic(self) -> None:
        suite, digest = load_suite(CONTRACT_SUITE)
        first = run_suite(suite, digest, DeterministicAdapter(), source_root=PACKAGE_ROOT)
        second = run_suite(suite, digest, DeterministicAdapter(), source_root=PACKAGE_ROOT)
        self.assertEqual(first["outcome_digest"], second["outcome_digest"])

    def test_cross_scope_leak_disqualifies_result(self) -> None:
        suite, digest = load_suite(CONTRACT_SUITE)
        result = run_suite(
            suite,
            digest,
            DeterministicAdapter(leak_scopes=True),
            source_root=PACKAGE_ROOT,
        )
        self.assertFalse(result["conformant"])
        self.assertIn("project-scope-isolation", result["disqualifying_failures"])

    def test_required_capability_skip_prevents_conformance(self) -> None:
        suite = {
            "schema_version": "0.1",
            "suite_id": "missing-capability",
            "dataset_version": "0.1.0",
            "description": "test",
            "profile": "contract",
            "default_k": 1,
            "cases": [
                {
                    "id": "requires-unknown",
                    "category": "test",
                    "description": "test",
                    "security_gate": False,
                    "required_capabilities": ["unknown"],
                    "operations": [{"op": "recall", "query": {"text": "test"}}],
                }
            ],
        }
        result = run_suite(suite, "0" * 64, DeterministicAdapter(), source_root=PACKAGE_ROOT)
        self.assertFalse(result["conformant"])
        self.assertEqual(result["required_skips"], ["requires-unknown"])

    def test_write_result_is_valid_json(self) -> None:
        suite, digest = load_suite(CONTRACT_SUITE)
        result = run_suite(suite, digest, DeterministicAdapter(), source_root=PACKAGE_ROOT)
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "result.json"
            write_result(output, result)
            loaded = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(loaded["outcome_digest"], result["outcome_digest"])

    def test_duplicate_case_id_is_invalid(self) -> None:
        suite, _ = load_suite(CONTRACT_SUITE)
        suite["cases"].append(suite["cases"][0])
        with self.assertRaises(SuiteError):
            run_suite(suite, "0" * 64, DeterministicAdapter(), source_root=PACKAGE_ROOT)


if __name__ == "__main__":
    unittest.main()
