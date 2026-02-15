from datetime import datetime, timezone
from unittest.mock import MagicMock, Mock, patch, call
import pytest

from app.services.project_service import ProjectService
from app.schemas.projects_schemas import ProjectCreate, ProjectResponse, ProjectsScope
from app.core.exceptions import AlreadyExistsError


@pytest.fixture
def project_repo():
    return MagicMock()


@pytest.fixture
def membership_repo():
    return MagicMock()


@pytest.fixture
def project_service(project_repo, membership_repo):
    return ProjectService(project_repo, membership_repo)


@pytest.fixture
def fake_project():
    project = Mock()
    project.id = 1
    project.name = "Test Project"
    project.description = "Test Description"
    project.api_key = "test_api_key_123"
    project.created_at = datetime(2026, 2, 1, tzinfo=timezone.utc)
    return project


@pytest.fixture
def fake_member_project():
    """Проект, де поточний користувач — viewer, а не owner."""
    project = Mock()
    project.id = 10
    project.name = "Shared Analytics"
    project.description = "Shared with me"
    project.api_key = "member_api_key_456"
    project.created_at = datetime(2026, 2, 10, tzinfo=timezone.utc)
    return project


class TestProjectCreate:
    @patch(
        "app.services.project_service.generate_api_key", return_value="test_api_key_123"
    )
    def test_create_success(
        self,
        mock_gen_api_key: Mock,
        project_repo: MagicMock,
        membership_repo: MagicMock,
        project_service: ProjectService,
        fake_project: Mock,
    ) -> None:
        project_repo.get_by_user_id.return_value = None
        project_repo.create.return_value = fake_project
        payload = ProjectCreate(name="Test Project", description="Test Description")

        result = project_service.create(user_id=1, payload=payload)

        assert isinstance(result, ProjectResponse)
        assert result.id == 1
        assert result.name == "Test Project"
        assert result.api_key == "test_api_key_123"
        project_repo.get_by_user_id.assert_called_once_with(
            user_id=1, project_name="Test Project", role="owner"
        )
        mock_gen_api_key.assert_called_once()
        project_repo.create.assert_called_once()
        membership_repo.create.assert_called_once()
        membership_repo.commit.assert_called_once()
        project_repo.commit.assert_called_once()

    @patch(
        "app.services.project_service.generate_api_key", return_value="test_api_key_123"
    )
    def test_create_already_exists(
        self,
        mock_gen_api_key: Mock,
        project_repo: MagicMock,
        membership_repo: MagicMock,
        project_service: ProjectService,
        fake_project: Mock,
    ) -> None:
        project_repo.get_by_user_id.return_value = fake_project

        payload = ProjectCreate(name="Test Project", description="Test Description")

        with pytest.raises(AlreadyExistsError, match="already exists"):
            project_service.create(user_id=1, payload=payload)
        mock_gen_api_key.assert_not_called()
        project_repo.create.assert_not_called()
        membership_repo.create.assert_not_called()


class TestProjectGetAll:
    def test_get_all_own_projects(
        self,
        project_repo: MagicMock,
        membership_repo: MagicMock,
        project_service: ProjectService,
        fake_project: Mock,
    ) -> None:
        project_repo.get_by_user_id.return_value = [fake_project]

        result = project_service.get_all(user_id=1, scope=ProjectsScope.OWN)

        assert len(result) == 1
        assert result[0].id == 1
        assert result[0].name == "Test Project"
        project_repo.get_by_user_id.assert_called_once_with(
            user_id=1, project_name=None, role="owner"
        )

    def test_get_all_member_projects(
        self,
        project_repo: MagicMock,
        membership_repo: MagicMock,
        project_service: ProjectService,
        fake_member_project: Mock,
    ) -> None:
        project_repo.get_by_user_id.return_value = [fake_member_project]

        result = project_service.get_all(user_id=1, scope=ProjectsScope.MEMBER)

        assert len(result) == 1
        assert result[0].id != 1
        assert result[0].id == fake_member_project.id
        assert result[0].name == "Shared Analytics"
        project_repo.get_by_user_id.assert_called_once_with(
            user_id=1, project_name=None, role="viewer"
        )

    def test_member_scope_does_not_return_own_projects(
        self,
        project_repo: MagicMock,
        membership_repo: MagicMock,
        project_service: ProjectService,
    ) -> None:
        """Scope MEMBER фільтрує по role='viewer', а не 'owner'."""
        project_repo.get_by_user_id.return_value = []

        project_service.get_all(user_id=1, scope=ProjectsScope.MEMBER)

        call_kwargs = project_repo.get_by_user_id.call_args
        assert call_kwargs.kwargs["role"] == "viewer"
        assert call_kwargs.kwargs["role"] != "owner"

    def test_get_all_empty(
        self,
        project_repo: MagicMock,
        membership_repo: MagicMock,
        project_service: ProjectService,
    ) -> None:
        project_repo.get_by_user_id.return_value = []

        result = project_service.get_all(user_id=404, scope=ProjectsScope.OWN)

        assert result == []
        project_repo.get_by_user_id.assert_called_once()
