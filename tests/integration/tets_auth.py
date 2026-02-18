import pytest
from fastapi.testclient import TestClient
from fastapi import status

from ..factories import make_user

@pytest.mark.integration
class TetsAuthRegister:
    def test_register_success(self, client: TestClient):
        user_password = "secret123"
        fake_user = make_user()
        response = client.post(
            "auth/register",
            json={
                "email": fake_user.email,
                "username": fake_user.username,
                "password": user_password
            }
        )
        body = response.json()
        assert response.status_code == status.HTTP_201_CREATED
        assert body["email"] == fake_user.email
        assert "password" not in body

    def test_register_exist_user(self, client: TestClient):
        user_password = "fake_password"
        user = make_user(password=user_password)

        client.post(
            "/auth/register",
            json={
                "email": user.email,
                "username": user.username,
                "password": user_password
            }
        )

        response = client.post(
            "/auth/register",
            json={
                "email": user.email,
                "username": user.username,
                "password": user_password
            }
        )
        assert response.status_code == status.HTTP_409_CONFLICT
        assert "already exists" in response.json()["detail"]

    def test_register_invalid_email(self, client: TestClient):
        response = client.post(
            "/auth/register",
            json={
                "email": "invalid email...",
                "username": "username",
                "password": "secret123"
            }
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
        assert "value is not a valid email" in response.text

class TetsAuthLogin:
    def tets_login_success(self, client: TestClient):
        pass

