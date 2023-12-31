# chat_app/tests/test_main.py

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello nddr"}

def test_error_400():
    response = client.get("/error400")
    assert response.status_code == 400
    assert response.json() == {"detail": "Bad Request"}

def test_error_403():
    response = client.get("/error403")
    assert response.status_code == 403
    assert response.json() == {"detail": "Forbidden"}
