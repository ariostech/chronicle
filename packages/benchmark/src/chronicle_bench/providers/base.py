"""Adapter contract for benchmark subjects."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class ProviderError(RuntimeError):
    """A provider failed explicitly rather than returning benchmark data."""


class OperationRejected(ProviderError):
    """A requested operation was deliberately denied."""


class BenchmarkAdapter(ABC):
    name = "abstract"
    version = "0"
    capabilities: frozenset[str] = frozenset()

    @abstractmethod
    def reset(self, case_id: str) -> None:
        """Reset isolated state before a case."""

    @abstractmethod
    def execute(self, operation: dict[str, Any]) -> dict[str, Any]:
        """Execute one fixture operation and return a normalized result."""

    def configuration(self) -> dict[str, str]:
        """Return a non-secret allowlist used only for result fingerprinting."""
        return {}
