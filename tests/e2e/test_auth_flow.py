from urllib import response
import pytest
from fastapi.testclient import TestClient
from fastapi import status

from app.schemas.user_schemas import UserMetaName
from ..factories import make_user


@pytest.mark.e2e
class TestClientAuthentication:
    def test_register_and_login_flow(self, client: TestClient) -> None:
        register_response = client.post(
            "/auth/register",
            json={
                "email": "jefry@gmail.com",
                "username": "littlestjeff1",
                "password": "1234567890",
            },
        )
        assert register_response.status_code == status.HTTP_201_CREATED
        user = register_response.json()
        assert user["email"] == "jefry@gmail.com"
        assert user["username"] == "littlestjeff1"
        assert "password" not in user

        login_response = client.post(
            "/auth/login",
            data={
                "username": user["email"],
                "password": "1234567890"
            }
        )
        assert login_response.status_code == status.HTTP_200_OK
        token = login_response.json()
        assert "access_token" in token
        assert token["token_type"] == "bearer"
        assert "refresh_token" in login_response.cookies

        me_response = client.get(
            "/users/me",
            headers={
                "Authorization": f"Bearer {token["access_token"]}"
            }
        )
        me = me_response.json()
        assert me_response.status_code == status.HTTP_200_OK
        assert me["id"] == user["id"]
        assert me["email"] == user["email"]

    def test_login_invalid_password(self, client: TestClient):
            user = make_user()
            client.post(
                "/auth/register",
                json={
                    "email": user.email,
                    "username": user.username,
                    "password": "Password",
                },
            )

            response = client.post(
                "/auth/login",
                data={
                    "username": user.email,
                    "password": "WrongPassword",
                },
            )
            assert response.status_code == 401
            assert "Invalid credentials" in response.text
