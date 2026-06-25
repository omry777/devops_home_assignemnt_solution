import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)
FIXTURES_DIR = Path(__file__).parent / "fixtures"


def load_epoch_cases() -> list[dict[str, object]]:
    with (FIXTURES_DIR / "epoch_cases.json").open() as fixture:
        return json.load(fixture)


@pytest.mark.parametrize("case", load_epoch_cases(), ids=lambda case: str(case["name"]))
def test_epoch_returns_expected_values_from_mock_data(case: dict[str, object]) -> None:
    response = client.post("/epoch", json={"date": case["date"]})

    assert response.status_code == 200
    assert response.json() == {"epoch": case["epoch"]}


def test_epoch_rejects_missing_date() -> None:
    response = client.post("/epoch", json={})

    assert response.status_code == 422


def test_epoch_rejects_invalid_date() -> None:
    response = client.post("/epoch", json={"date": "tomorrow morning"})

    assert response.status_code == 422


def test_epoch_rejects_naive_timestamp() -> None:
    response = client.post("/epoch", json={"date": "2026-06-15T10:00:00"})

    assert response.status_code == 200
