# import pytest
from main import app
from fastapi.testclient import TestClient
from config import Config

client = TestClient(app)


def test_invalid_request_body():
    request_data = {
        "Pclass": 1,
        "Sex": 0,
        "Age": 29,
        "SibSp": 0,
        "Parch": 0,
        "Fare": 100,
        "Embarked": "C"
    }

    response = client.post("/api/v1/predict", json=request_data, headers={"X-API-KEY" : Config.API_KEY})
    assert response.status_code == 422


def test_valid_body():
    request_data = {
        "Pclass": 1,
        "Sex": "male",
        "Age": 29,
        "SibSp": 0,
        "Parch": 0,
        "Fare": 100,
        "Embarked": "C"
    }

    response = client.post("/api/v1/predict", json=request_data, headers={"X-API-KEY" : Config.API_KEY})
    assert response.status_code == 200
    json_response = response.json()
    assert "Survived" in json_response
    assert json_response["Survived"] in ["Yes", "No"]
