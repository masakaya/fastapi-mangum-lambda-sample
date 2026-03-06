from fastapi.testclient import TestClient

from src.controllers.users import _user_repository
from src.main import app

client = TestClient(app)


def setup_function():
    """各テスト前にリポジトリをリセットする."""
    _user_repository._store.clear()
    _user_repository._next_id = 1


def test_get_users_empty():
    response = client.get("/users")
    assert response.status_code == 200
    assert response.json() == []


def test_create_user():
    response = client.post("/users", json={"name": "Alice", "email": "alice@example.com"})
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Alice"
    assert data["email"] == "alice@example.com"


def test_get_users_after_create():
    client.post("/users", json={"name": "Bob", "email": "bob@example.com"})
    response = client.get("/users")
    assert response.status_code == 200
    users = response.json()
    assert len(users) == 1
    assert users[0]["name"] == "Bob"


def test_get_user_by_id():
    client.post("/users", json={"name": "Charlie", "email": "charlie@example.com"})
    response = client.get("/users/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Charlie"


def test_get_user_not_found():
    response = client.get("/users/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}
