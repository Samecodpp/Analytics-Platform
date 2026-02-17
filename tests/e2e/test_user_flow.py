import pytest
from fastapi import status
from fastapi.testclient import TestClient


@pytest.mark.e2e
class TestUserFlow:
    """E2E tests for user endpoints"""

    def _register_and_login(self, client: TestClient) -> tuple[dict, str]:
        register_resp = client.post(
            "/auth/register",
            json={
                "email": "testuser@example.com",
                "username": "testuser",
                "password": "SecurePass123",
            },
        )
        assert register_resp.status_code == status.HTTP_201_CREATED
        user = register_resp.json()

        login_resp = client.post(
            "/auth/login",
            data={
                "username": user["email"],
                "password": "SecurePass123",
            },
        )
        assert login_resp.status_code == status.HTTP_200_OK
        tokens = login_resp.json()

        return user, tokens["access_token"]

    def test_user_get_current_user(self, client: TestClient):
        user, access_token = self._register_and_login(client)

        me_resp = client.get(
            "/users/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        assert me_resp.status_code == status.HTTP_200_OK
        me = me_resp.json()
        assert me["id"] == user["id"]
        assert me["email"] == user["email"]
        assert me["username"] == user["username"]

    def test_user_update_info(self, client: TestClient):
        user, access_token = self._register_and_login(client)

        update_resp = client.patch(
            "/users/me",
            headers={"Authorization": f"Bearer {access_token}"},
            json={
                "username": "updated_user",
                "first_name": "John",
                "last_name": "Doe",
            },
        )
        assert update_resp.status_code == status.HTTP_200_OK
        updated_user = update_resp.json()
        assert updated_user["username"] == "updated_user"
        assert updated_user["first_name"] == "John"
        assert updated_user["last_name"] == "Doe"
        assert updated_user["id"] == user["id"]

    def test_user_succes_flow(self, client: TestClient):
        register_resp = client.post(
            "/auth/register",
            json={
                "email": "fullflow@example.com",
                "username": "flowuser",
                "password": "SecurePass123",
            },
        )
        assert register_resp.status_code == status.HTTP_201_CREATED
        user = register_resp.json()
        user_id = user["id"]

        login_resp = client.post(
            "/auth/login",
            data={"username": user["email"], "password": "SecurePass123"},
        )
        assert login_resp.status_code == status.HTTP_200_OK
        access_token = login_resp.json()["access_token"]

        me_resp = client.get(
            "/users/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        assert me_resp.status_code == status.HTTP_200_OK
        me = me_resp.json()
        assert me["id"] == user_id
        assert me["email"] == "fullflow@example.com"

        update_resp = client.patch(
            "/users/me",
            headers={"Authorization": f"Bearer {access_token}"},
            json={
                "first_name": "Flow",
                "last_name": "User",
            },
        )
        assert update_resp.status_code == status.HTTP_200_OK
        updated = update_resp.json()
        assert updated["first_name"] == "Flow"
        assert updated["last_name"] == "User"
        assert updated["id"] == user_id

    def test_user_unauthorized_access(self, client: TestClient):
        resp = client.get("/users/me")
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    def test_user_invalid_token_access(self, client: TestClient):
        resp = client.get(
            "/users/me",
            headers={"Authorization": "Bearer invalid_token_xyz"},
        )
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED
