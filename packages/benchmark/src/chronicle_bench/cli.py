"""Command-line interface for Chronicle benchmark suites."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from chronicle_bench.providers import DeterministicAdapter, HindsightAdapter
from chronicle_bench.runner import SuiteError, load_suite, run_suite, write_result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="chronicle-bench")
    subparsers = parser.add_subparsers(dest="command", required=True)
    run = subparsers.add_parser("run", help="run a versioned benchmark suite")
    run.add_argument("--suite", type=Path, required=True)
    run.add_argument("--adapter", choices=("deterministic", "hindsight"), default="deterministic")
    run.add_argument("--output", type=Path)
    run.add_argument("--seed", type=int, default=0)
    run.add_argument("--subject-version")
    run.add_argument("--model-id", default="none")
    run.add_argument("--configuration-label", default="default")
    run.add_argument("--quiet", action="store_true")
    return parser


def _adapter(name: str):
    if name == "deterministic":
        return DeterministicAdapter()
    return HindsightAdapter.from_environment()


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        suite, digest = load_suite(args.suite)
        result = run_suite(
            suite,
            digest,
            _adapter(args.adapter),
            seed=args.seed,
            source_root=Path.cwd(),
            subject_version=args.subject_version,
            model_id=args.model_id,
            configuration_label=args.configuration_label,
        )
        if args.output:
            write_result(args.output, result)
        if not args.quiet:
            print(
                json.dumps(
                    {
                        "suite": result["suite"]["id"],
                        "adapter": result["subject"]["adapter"],
                        "passed": result["aggregates"]["passed"],
                        "failed": result["aggregates"]["failed"],
                        "skipped": result["aggregates"]["skipped"],
                        "conformant": result["conformant"],
                        "outcome_digest": result["outcome_digest"],
                        "output": str(args.output) if args.output else None,
                    },
                    indent=2,
                )
            )
        return 0 if result["conformant"] else 2
    except (OSError, ValueError, SuiteError) as exc:
        print(f"chronicle-bench: {exc}", file=sys.stderr)
        return 1
