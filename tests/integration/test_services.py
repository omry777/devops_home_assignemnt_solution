import json
import re
import time
import urllib.error
import urllib.request


def read_json(url: str) -> dict[str, object]:
    with urllib.request.urlopen(url, timeout=3) as response:
        return json.loads(response.read().decode("utf-8"))


def wait_for_json(url: str, timeout_seconds: int = 90) -> dict[str, object]:
    deadline = time.time() + timeout_seconds
    last_error: Exception | None = None

    while time.time() < deadline:
        try:
            return read_json(url)
        except (OSError, urllib.error.HTTPError) as error:
            last_error = error
            time.sleep(1)

    raise AssertionError(f"{url} did not become ready: {last_error}")


def test_now_time_service_calls_epoch_service() -> None:
    assert wait_for_json("http://localhost:8081/health") == {"status": "ok"}

    payload = wait_for_json("http://localhost:8080/now")
    message = payload.get("message")

    assert isinstance(message, str)
    assert re.fullmatch(r"now is \d+", message)

    epoch = int(message.rsplit(" ", maxsplit=1)[1])
    assert abs(time.time() - epoch) < 30
