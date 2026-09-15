"""Small, dependency-free ranking metrics used by Chronicle benchmarks."""

from __future__ import annotations

import math
from collections.abc import Sequence


def _unique_prefix(ranked_ids: Sequence[str], k: int) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item_id in ranked_ids[: max(k, 0)]:
        if item_id not in seen:
            seen.add(item_id)
            result.append(item_id)
    return result


def precision_at_k(ranked_ids: Sequence[str], relevant_ids: set[str], k: int) -> float:
    returned = _unique_prefix(ranked_ids, k)
    if not returned:
        return 1.0 if not relevant_ids else 0.0
    return sum(item_id in relevant_ids for item_id in returned) / len(returned)


def recall_at_k(ranked_ids: Sequence[str], relevant_ids: set[str], k: int) -> float:
    returned = set(_unique_prefix(ranked_ids, k))
    if not relevant_ids:
        return 1.0 if not returned else 0.0
    return len(returned & relevant_ids) / len(relevant_ids)


def reciprocal_rank(ranked_ids: Sequence[str], relevant_ids: set[str], k: int) -> float:
    for rank, item_id in enumerate(_unique_prefix(ranked_ids, k), start=1):
        if item_id in relevant_ids:
            return 1.0 / rank
    return 0.0


def ndcg_at_k(ranked_ids: Sequence[str], relevant_ids: set[str], k: int) -> float:
    returned = _unique_prefix(ranked_ids, k)
    dcg = sum(
        1.0 / math.log2(rank + 1)
        for rank, item_id in enumerate(returned, start=1)
        if item_id in relevant_ids
    )
    ideal_hits = min(len(relevant_ids), max(k, 0))
    if ideal_hits == 0:
        return 1.0 if not returned else 0.0
    ideal = sum(1.0 / math.log2(rank + 1) for rank in range(1, ideal_hits + 1))
    return dcg / ideal


def percentile(values: Sequence[float], percentile_value: float) -> float:
    if not values:
        return 0.0
    if not 0.0 <= percentile_value <= 100.0:
        raise ValueError("percentile must be between 0 and 100")
    ordered = sorted(values)
    index = max(0, math.ceil((percentile_value / 100.0) * len(ordered)) - 1)
    return ordered[index]
