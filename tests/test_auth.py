import os
os.environ["DATABASE_URL"] = "sqlite:///./test_auth.db"
os.environ["JWT_SECRET"] = "test-secret"

from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine

client = TestClient(app)

def setup_module():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

def test_register_login_and_me():
    register = client.post("/auth/register", json={
        "username": "kadija",
        "password": "StrongPass123!"
    })
    assert register.status_code == 201
    assert "password_hash" not in register.text

    login = client.post("/auth/login", json={
        "username": "kadija",
        "password": "StrongPass123!"
    })
    assert login.status_code == 200

    token = login.json()["access_token"]
    me = client.get("/me", headers={"Authorization": f"Bearer {token}"})
    assert me.status_code == 200
    assert me.json()["username"] == "kadija"

def test_non_admin_cannot_access_admin_route():
    login = client.post("/auth/login", json={
        "username": "kadija",
        "password": "StrongPass123!"
    })
    token = login.json()["access_token"]
    response = client.get("/admin/users", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403
