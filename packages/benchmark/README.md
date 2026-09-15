# Chronicle benchmark harness

This package executes Chronicle's versioned memory and governance evaluation suites. It currently includes:

- a deterministic contract adapter for lifecycle and security semantics;
- an opt-in Hindsight adapter for live retain/recall evaluation;
- synthetic v0.1 fixtures;
- precision, recall, MRR, nDCG, provenance, latency, and policy metrics;
- machine-readable result artifacts and deterministic outcome digests.

Read the normative [Benchmark Specification](../../docs/spec/BENCHMARK.md) before adding fixtures or publishing results.

## Requirements

- Python 3.11 or later
- no third-party runtime packages

## Run the contract suite

From the repository root:

```bash
PYTHONPATH=packages/benchmark/src \
  python3 -m chronicle_bench run \
  --suite packages/benchmark/fixtures/v0.1/contract.json \
  --output tmp/benchmark-result.json
```

The command exits `0` when all required cases and security gates pass, `2` when evaluation completes without conformance, and `1` for invalid input or runner errors.

Use `--quiet` in CI. Result JSON is still written when `--output` is provided.

## Run the tests

```bash
PYTHONPATH=packages/benchmark/src \
  python3 -m unittest discover -s packages/benchmark/tests -v
```

## Live Hindsight run

Hindsight execution is deliberately opt-in. Use a disposable, non-production bank.

```bash
export HINDSIGHT_BASE_URL=http://localhost:8888
export HINDSIGHT_BANK_ID=chronicle-benchmark-local
export HINDSIGHT_API_TOKEN=replace-if-required

PYTHONPATH=packages/benchmark/src \
  python3 -m chronicle_bench run \
  --adapter hindsight \
  --suite packages/benchmark/fixtures/v0.1/provider-retrieval.json \
  --output tmp/hindsight-result.json
```

The adapter maps Chronicle fixture identifiers into provider metadata and accepts common Hindsight response envelopes. It reports only provider-retrieval behavior. It does not claim Chronicle gateway conformance.

Environment values are not written to results. The runner records a hash of a redacted configuration allowlist.

## Add a case

1. Add the case to a new dataset version when expected outcomes change.
2. Give the case a stable ID and explicit required capabilities.
3. Mark policy and isolation cases as security gates.
4. Use invented data only.
5. Add a focused unit test when the case introduces new runner behavior.
6. Run the policy checker and full test suite.

Do not copy third-party benchmark datasets into this repository without a license and attribution review.
