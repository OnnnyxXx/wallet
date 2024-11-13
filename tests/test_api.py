import pytest
from main import app
from fastapi.testclient import TestClient


@pytest.fixture(scope='session')
def test_app():
    with TestClient(app) as client:
        yield client


# def test_create_wallet(test_app):
#     uuid = "6"
#
#     response = test_app.post('/api/v1/wallets/', json={"uuid": uuid})
#     assert response.status_code == 200
#     assert response.json() == {"uuid": uuid, "balance": 0.0}


def test_operation_wallet(test_app):
    response = test_app.post("/api/v1/wallets/1/operation",
                             json={"operationType": "DEPOSIT", "amount": 1000000})
    assert response.status_code == 200


def test_get_wallet(test_app):
    response = test_app.get("/api/v1/wallets/1")
    assert response.status_code == 200
