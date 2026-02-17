import pytest
from fastapi import status
from fastapi.testclient import TestClient


@pytest.mark.e2e
class TestProjectFlow:
    def _register_and_login(self, client: TestClient) -> tuple[dict, str]:
        register_resp = client.post(
            "/auth/register",
            json={
                "email": "projectuser@example.com",
                "username": "projectuser",
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

    def test_create_project_success(self, client: TestClient):
        _, access_token = self._register_and_login(client)

        create_resp = client.post(
            "/projects/",
            headers={"Authorization": f"Bearer {access_token}"},
            json={
                "name": "Analytics Dashboard",
                "description": "Main analytics dashboard project",
            },
        )
        assert create_resp.status_code == status.HTTP_201_CREATED
        project = create_resp.json()
        assert project["name"] == "Analytics Dashboard"
        assert project["description"] == "Main analytics dashboard project"
        assert project["id"] is not None
        assert project["api_key"] is not None
        assert len(project["api_key"]) > 10

    def test_create_project_duplicate_name(self, client: TestClient):
        _, access_token = self._register_and_login(client)

        client.post(
            "/projects/",
            headers={"Authorization": f"Bearer {access_token}"},
            json={
                "name": "Duplicate Name",
                "description": "First project",
            },
        )

        dup_resp = client.post(
            "/projects/",
            headers={"Authorization": f"Bearer {access_token}"},
            json={
                "name": "Duplicate Name",
                "description": "Second project",
            },
        )
        assert dup_resp.status_code == status.HTTP_409_CONFLICT
        assert "already exists" in dup_resp.json()["detail"]

    def test_get_projects_all(self, client: TestClient):
        _, access_token = self._register_and_login(client)

        client.post(
            "/projects/",
            headers={"Authorization": f"Bearer {access_token}"},
            json={"name": "Project 1", "description": "First"},
        )
        client.post(
            "/projects/",
            headers={"Authorization": f"Bearer {access_token}"},
            json={"name": "Project 2", "description": "Second"},
        )

        list_resp = client.get(
            "/projects/?scope=all",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        assert list_resp.status_code == status.HTTP_200_OK
        projects = list_resp.json()
        assert len(projects) == 2
        assert projects[0]["name"] == "Project 1"
        assert projects[1]["name"] == "Project 2"

    def test_get_projects_own(self, client: TestClient):
        _, access_token = self._register_and_login(client)

        client.post(
            "/projects/",
            headers={"Authorization": f"Bearer {access_token}"},
            json={"name": "Owned Project", "description": "My project"},
        )

        list_resp = client.get(
            "/projects/?scope=own",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        assert list_resp.status_code == status.HTTP_200_OK
        projects = list_resp.json()
        assert len(projects) >= 1
        assert any(p["name"] == "Owned Project" for p in projects)

    def test_get_projects_empty(self, client: TestClient):
        _, access_token = self._register_and_login(client)

        list_resp = client.get(
            "/projects/",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        assert list_resp.status_code == status.HTTP_200_OK
        projects = list_resp.json()
        assert isinstance(projects, list)
        assert len(projects) == 0

    def test_project_success_flow(self, client: TestClient):
        user, access_token = self._register_and_login(client)

        create_resp = client.post(
            "/projects/",
            headers={"Authorization": f"Bearer {access_token}"},
            json={
                "name": "Complete Flow Project",
                "description": "Testing full flow",
            },
        )
        assert create_resp.status_code == status.HTTP_201_CREATED
        project = create_resp.json()
        project_id = project["id"]
        api_key = project["api_key"]

        list_resp = client.get(
            "/projects/?scope=all",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        assert list_resp.status_code == status.HTTP_200_OK
        projects = list_resp.json()
        assert any(p["id"] == project_id for p in projects)

        found_project = next((p for p in projects if p["id"] == project_id), None)
        assert found_project is not None
        assert found_project["name"] == "Complete Flow Project"
        assert found_project["description"] == "Testing full flow"
        assert found_project["api_key"] == api_key

    def test_project_unauthorized_access(self, client: TestClient):
        resp = client.get("/projects/")
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    def test_project_invalid_token(self, client: TestClient):
        resp = client.get(
            "/projects/",
            headers={"Authorization": "Bearer invalid_token"},
        )
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    def test_project_different_users_independent(self, client: TestClient):
        register1 = client.post(
            "/auth/register",
            json={
                "email": "user1@example.com",
                "username": "user1",
                "password": "SecurePass123",
            },
        )
        user1 = register1.json()
        login1 = client.post(
            "/auth/login",
            data={"username": user1["email"], "password": "SecurePass123"},
        )
        token1 = login1.json()["access_token"]

        client.post(
            "/projects/",
            headers={"Authorization": f"Bearer {token1}"},
            json={"name": "User1 Project", "description": "User 1"},
        )

        register2 = client.post(
            "/auth/register",
            json={
                "email": "user2@example.com",
                "username": "user2",
                "password": "SecurePass123",
            },
        )
        user2 = register2.json()
        login2 = client.post(
            "/auth/login",
            data={"username": user2["email"], "password": "SecurePass123"},
        )
        token2 = login2.json()["access_token"]

        client.post(
            "/projects/",
            headers={"Authorization": f"Bearer {token2}"},
            json={"name": "User2 Project", "description": "User 2"},
        )

        resp = client.post(
            "/projects/",
            headers={"Authorization": f"Bearer {token2}"},
            json={"name": "User1 Project", "description": "But different user"},
        )
        assert resp.status_code == status.HTTP_201_CREATED

        list1 = client.get(
            "/projects/?scope=own",
            headers={"Authorization": f"Bearer {token1}"},
        )
        user1_projects = list1.json()
        assert len(user1_projects) == 1
        assert user1_projects[0]["name"] == "User1 Project"

        list2 = client.get(
            "/projects/?scope=own",
            headers={"Authorization": f"Bearer {token2}"},
        )
        user2_projects = list2.json()
        assert len(user2_projects) == 2
        assert any(p["name"] == "User2 Project" for p in user2_projects)
