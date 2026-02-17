import pytest
from pytest_mock import MockerFixture

from tests.fakes.fake_user_repo import FakeUserRepo
from tests.factories import make_user
from app.services.user_service import UserService
from app.schemas.user_schemas import User, UserUpdate
from app.core.exceptions import NotFoundError


@pytest.fixture
def user_repo():
    return FakeUserRepo()


@pytest.fixture
def user_service(user_repo):
    return UserService(user_repo)


def _seed_user(repo: FakeUserRepo, **overrides):
    user = make_user(**overrides)
    repo._users[user.id] = user
    return user

@pytest.mark.unit
class TestUserGetByID:
    def test_get_by_id_success(
        self, user_repo: FakeUserRepo, user_service: UserService
    ):
        seeded = _seed_user(
            user_repo, id=1, email="found@test.com", username="founduser"
        )

        result = user_service.get_by_id(1)

        assert isinstance(result, User)
        assert result.id == 1
        assert result.email == "found@test.com"

    def test_get_by_id_not_found(self, user_service: UserService):
        with pytest.raises(NotFoundError, match="not found"):
            user_service.get_by_id(404)

@pytest.mark.unit
class TestUserUpdateInfo:
    def test_update_info_success(
        self, user_repo: FakeUserRepo, user_service: UserService, mocker: MockerFixture
    ):
        spy_commit = mocker.spy(user_repo, "commit")
        _seed_user(user_repo, id=1, email="upd@test.com", username="old")

        result = user_service.update_info(
            1,
            UserUpdate(
                username="new_username",
                first_name="John",
                last_name="Doe",
            ),
        )

        assert isinstance(result, User)
        assert result.username == "new_username"
        assert result.first_name == "John"
        assert result.last_name == "Doe"
        spy_commit.assert_called_once()

        stored = user_repo.get_by_id(1)
        assert stored.username == "new_username"

    def test_update_info_not_found(
        self, user_service: UserService, mocker: MockerFixture, user_repo: FakeUserRepo
    ):
        spy_commit = mocker.spy(user_repo, "commit")

        with pytest.raises(NotFoundError, match="not found"):
            user_service.update_info(404, UserUpdate(username="new"))

        spy_commit.assert_not_called()

    def test_update_info_empty_data(
        self, user_repo: FakeUserRepo, user_service: UserService
    ):
        seeded = _seed_user(user_repo, id=1, email="empty@test.com", username="same")

        result = user_service.update_info(1, UserUpdate())

        assert isinstance(result, User)
        assert result.username == "same"
        assert result.email == "empty@test.com"
