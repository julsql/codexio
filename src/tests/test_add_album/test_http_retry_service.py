import unittest

from main.core.infrastructure.api.internal.http_retry_service import HttpRetryService


class TestHttpRetryService(unittest.TestCase):
    def test_returns_result_without_retrying(self):
        calls = []

        def operation():
            calls.append(1)
            return "ok"

        result = HttpRetryService.call(operation, retryable=(ConnectionError,), backoff_seconds=0)

        self.assertEqual("ok", result)
        self.assertEqual(1, len(calls))

    def test_retries_until_success(self):
        calls = []

        def operation():
            calls.append(1)
            if len(calls) < 3:
                raise ConnectionError("connexion coupée")
            return "ok"

        result = HttpRetryService.call(operation, retryable=(ConnectionError,), backoff_seconds=0)

        self.assertEqual("ok", result)
        self.assertEqual(3, len(calls))

    def test_raises_last_error_when_all_attempts_fail(self):
        calls = []

        def operation():
            calls.append(1)
            raise TimeoutError(f"timeout {len(calls)}")

        with self.assertRaises(TimeoutError) as context:
            HttpRetryService.call(operation, retryable=(TimeoutError,), attempts=3, backoff_seconds=0)

        self.assertEqual("timeout 3", str(context.exception))
        self.assertEqual(3, len(calls))

    def test_does_not_retry_unexpected_error(self):
        calls = []

        def operation():
            calls.append(1)
            raise ValueError("réponse illisible")

        with self.assertRaises(ValueError):
            HttpRetryService.call(operation, retryable=(ConnectionError,), backoff_seconds=0)

        self.assertEqual(1, len(calls))


if __name__ == "__main__":
    unittest.main()
