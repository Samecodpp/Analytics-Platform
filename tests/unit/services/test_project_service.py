import pytest
from pytest_mock import MockerFixture

from tests.fakes.fake_project_repo import FakeProjectRepo
from tests.fakes.fake_membership_repo import FakeMembershipRepo
from tests.factories import make_project
from app.services.project_service import ProjectService
from app.schemas.projects_schemas import ProjectCreate, ProjectResponse, ProjectsScope
from app.core.exceptions import AlreadyExistsError, InvalidCreateError


@pytest.fixture
def shared_memberships():
    return []


@pytest.fixture
def project_repo(shared_memberships):
    return FakeProjectRepo(membership_store=shared_memberships)


@pytest.fixture
def membership_repo(shared_memberships):
    return FakeMembershipRepo(membership_store=shared_memberships)


@pytest.fixture
def project_service(project_repo, membership_repo):
    return ProjectService(project_repo, membership_repo)

@pytest.mark.unit
class TestProjectCreate:
    def test_create_success(
        self,
        project_repo: FakeProjectRepo,
        membership_repo: FakeMembershipRepo,
        project_service: ProjectService,
        mocker: MockerFixture,
    ):
        spy_proj_commit = mocker.spy(project_repo, "commit")
        spy_memb_commit = mocker.spy(membership_repo, "commit")
        payload = ProjectCreate(name="Test Project", description="Test Description")

        result = project_service.create(user_id=1, payload=payload)

        assert isinstance(result, ProjectResponse)
        assert result.name == "Test Project"
        assert result.description == "Test Description"
        assert result.api_key is not None
        assert len(result.api_key) > 10

        memberships = membership_repo.get_by_project_id(result.id)
        assert len(memberships) == 1
        assert memberships[0].user_id == 1
        assert memberships[0].role == "owner"
        spy_proj_commit.assert_called_once()
        spy_memb_commit.assert_called_once()

    def test_create_duplicate_name(
        self,
        project_repo: FakeProjectRepo,
        project_service: ProjectService,
    ):
        project_service.create(
            user_id=1, payload=ProjectCreate(name="Duplicate", description="First")
        )

        with pytest.raises(AlreadyExistsError, match="already exists"):
            project_service.create(
                user_id=1, payload=ProjectCreate(name="Duplicate", description="Second")
            )

    def test_create_invalid(
        self,
        project_repo: FakeProjectRepo,
        project_service: ProjectService,
        mocker: MockerFixture,
    ):
        mocker.patch.object(project_repo, "create", return_value=None)

        with pytest.raises(InvalidCreateError, match="Could not create project"):
            project_service.create(
                user_id=1, payload=ProjectCreate(name="Broken", description="Fail")
            )

    def test_create_same_name_different_user(
        self,
        project_repo: FakeProjectRepo,
        project_service: ProjectService,
    ):
        result1 = project_service.create(
            user_id=1, payload=ProjectCreate(name="Analytics", description="User 1")
        )
        result2 = project_service.create(
            user_id=2, payload=ProjectCreate(name="Analytics", description="User 2")
        )

        assert result1.name == result2.name
        assert result1.id != result2.id

@pytest.mark.unit
class TestProjectGetAll:
    def _create_project_with_membership(
        self,
        project_repo: FakeProjectRepo,
        user_id: int,
        role: str,
        **project_overrides,
    ):
        project = make_project(**project_overrides)
        project_repo._projects[project.id] = project
        project_repo.add_membership(user_id=user_id, project_id=project.id, role=role)
        return project

    def test_get_own(
        self,
        project_repo: FakeProjectRepo,
        project_service: ProjectService,
    ):
        own = self._create_project_with_membership(
            project_repo, user_id=1, role="owner", name="My Project"
        )
        self._create_project_with_membership(
            project_repo, user_id=1, role="viewer", name="Shared Project"
        )

        result = project_service.get_all(user_id=1, scope=ProjectsScope.OWN)

        assert len(result) == 1
        assert result[0].name == "My Project"

    def test_get_member(
        self,
        project_repo: FakeProjectRepo,
        project_service: ProjectService,
    ):
        self._create_project_with_membership(
            project_repo, user_id=1, role="owner", name="My Project"
        )
        shared = self._create_project_with_membership(
            project_repo, user_id=1, role="viewer", name="Shared Project"
        )

        result = project_service.get_all(user_id=1, scope=ProjectsScope.MEMBER)

        assert len(result) == 1
        assert result[0].name == "Shared Project"

    def test_get_all(
        self,
        project_repo: FakeProjectRepo,
        project_service: ProjectService
    ):
        self._create_project_with_membership(
            project_repo, user_id=1, role="owner", name="My Project"
        )
        shared = self._create_project_with_membership(
            project_repo, user_id=1, role="viewer", name="Shared Project"
        )

        result = project_service.get_all(user_id=1, scope=ProjectsScope.ALL)
        names = [project.name for project in result]

        assert len(result) == 2
        assert "My Project" in names
        assert "Shared Project" in names

    def test_get_all_empty(self, project_service: ProjectService):
        result = project_service.get_all(user_id=404, scope=ProjectsScope.OWN)

        assert result == []
