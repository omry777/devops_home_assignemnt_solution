from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_epoch_accepts_utc_timestamp() -> None:
    response = client.post("/epoch", json={"date": "2026-06-15T10:00:00Z"})

    assert response.status_code == 200
    assert response.json() == {"epoch": 1781517600}


def test_epoch_accepts_timezone_offset() -> None:
    response = client.post("/epoch", json={"date": "2026-06-15T13:00:00+03:00"})

    assert response.status_code == 200
    assert response.json() == {"epoch": 1781517600}


def test_epoch_rejects_missing_date() -> None:
    response = client.post("/epoch", json={})

    assert response.status_code == 422


def test_epoch_rejects_invalid_date() -> None:
    response = client.post("/epoch", json={"date": "tomorrow morning"})

    assert response.status_code == 422


def test_epoch_rejects_naive_timestamp() -> None:
    response = client.post("/epoch", json={"date": "2026-06-15T10:00:00"})

    assert response.status_code == 422
