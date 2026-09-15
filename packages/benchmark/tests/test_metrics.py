import unittest

from chronicle_bench.metrics import (
    ndcg_at_k,
    percentile,
    precision_at_k,
    recall_at_k,
    reciprocal_rank,
)


class MetricTests(unittest.TestCase):
    def test_rank_metrics(self) -> None:
        ranked = ["wrong", "right", "other"]
        relevant = {"right"}
        self.assertEqual(precision_at_k(ranked, relevant, 2), 0.5)
        self.assertEqual(recall_at_k(ranked, relevant, 2), 1.0)
        self.assertEqual(reciprocal_rank(ranked, relevant, 3), 0.5)
        self.assertGreater(ndcg_at_k(ranked, relevant, 3), 0.0)
        self.assertLess(ndcg_at_k(ranked, relevant, 3), 1.0)

    def test_empty_expected_and_empty_result_is_correct_abstention(self) -> None:
        self.assertEqual(precision_at_k([], set(), 5), 1.0)
        self.assertEqual(recall_at_k([], set(), 5), 1.0)
        self.assertEqual(ndcg_at_k([], set(), 5), 1.0)

    def test_empty_expected_with_result_is_not_correct_abstention(self) -> None:
        self.assertEqual(recall_at_k(["invented"], set(), 5), 0.0)
        self.assertEqual(ndcg_at_k(["invented"], set(), 5), 0.0)

    def test_duplicate_ids_do_not_inflate_precision(self) -> None:
        self.assertEqual(precision_at_k(["right", "right"], {"right"}, 2), 1.0)

    def test_nearest_rank_percentile(self) -> None:
        self.assertEqual(percentile([1, 2, 3, 4], 50), 2)
        self.assertEqual(percentile([1, 2, 3, 4], 95), 4)
        with self.assertRaises(ValueError):
            percentile([1], 101)


if __name__ == "__main__":
    unittest.main()
