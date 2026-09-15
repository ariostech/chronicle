import unittest

from chronicle_bench.providers.hindsight import HindsightAdapter


class HindsightAdapterTests(unittest.TestCase):
    def test_retain_request_carries_fixture_identity_without_token_leak(self) -> None:
        calls = []

        def fake_http(method, url, body, headers):
            calls.append((method, url, body, headers))
            return {"accepted": 1}

        adapter = HindsightAdapter(
            base_url="http://hindsight.test",
            bank_id="disposable-bank",
            api_token="test-token",
            http=fake_http,
        )
        adapter.reset("case-one")
        response = adapter.execute(
            {
                "op": "retain",
                "record": {
                    "id": "fact-one",
                    "text": "A synthetic fact.",
                    "scope": "benchmark:test",
                    "tags": ["chronicle-benchmark"],
                },
            }
        )
        self.assertTrue(response["accepted"])
        method, url, body, headers = calls[0]
        self.assertEqual(method, "POST")
        self.assertTrue(url.endswith("/v1/default/banks/disposable-bank/memories"))
        self.assertEqual(body["items"][0]["metadata"]["chronicle_fixture_id"], "fact-one")
        self.assertEqual(headers["Authorization"], "Bearer test-token")
        self.assertNotIn("test-token", str(adapter.configuration()))

    def test_recall_normalizes_nested_response(self) -> None:
        calls = []

        def fake_http(method, url, body, headers):
            calls.append((method, url, body, headers))
            return {
                "data": {
                    "results": [
                        {
                            "content": "A synthetic fact.",
                            "score": 0.92,
                            "document_id": "chronicle-bench:case-one:fact-one",
                            "metadata": {"chronicle_fixture_id": "fact-one"},
                        }
                    ]
                }
            }

        adapter = HindsightAdapter(
            base_url="http://hindsight.test",
            bank_id="disposable-bank",
            http=fake_http,
        )
        adapter.reset("case-one")
        result = adapter.execute(
            {
                "op": "recall",
                "query": {
                    "text": "synthetic fact",
                    "k": 3,
                    "tags": ["chronicle-benchmark", "case-one"],
                },
            }
        )
        self.assertEqual(result["items"][0]["id"], "fact-one")
        self.assertEqual(result["items"][0]["text"], "A synthetic fact.")
        self.assertGreater(result["context_tokens"], 0)
        self.assertEqual(calls[0][2]["tags_match"], "all_strict")

    def test_response_envelopes(self) -> None:
        expected = [{"id": "one"}]
        self.assertEqual(HindsightAdapter._extract_items(expected), expected)
        self.assertEqual(HindsightAdapter._extract_items({"memories": expected}), expected)
        self.assertEqual(HindsightAdapter._extract_items({"items": expected}), expected)
        self.assertEqual(HindsightAdapter._extract_items({}), [])


if __name__ == "__main__":
    unittest.main()
