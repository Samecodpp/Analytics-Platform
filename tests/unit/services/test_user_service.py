from datetime import datetime, timezone
from unittest.mock import MagicMock, Mock, patch
import pytest

from app.schemas.user_schemas import User, UserUpdate
from app.services.user_service import UserService
from app.core.exceptions import NotFoundError


@pytest.fixture
def user_repo():
    return MagicMock()


@pytest.fixture
def user_service(user_repo):
    return UserService(user_repo)


@pytest.fixture
def fake_user():
    user = Mock()
    user.id = 1
    user.email = "test@example.com"
    user.username = "testuser"
    user.first_name = None
    user.last_name = None
    user.created_at = datetime(2026, 1, 1, tzinfo=timezone.utc)
    return user


class TestUserGetByID:
    def test_get_by_id_success(
        self, user_repo: MagicMock, user_service: UserService, fake_user: Mock
    ) -> None:
        user_repo.get_by_id.return_value = fake_user

        result = user_service.get_by_id(1)

        assert isinstance(result, User)
        assert result.id == 1
        assert result.email == "test@example.com"

        user_repo.get_by_id.assert_called_once_with(1)

    def test_get_by_id_not_found(
        self,
        user_repo: MagicMock,
        user_service: UserService,
    ) -> None:
        user_repo.get_by_id.return_value = None

        with pytest.raises(NotFoundError, match="not found"):
            user_service.get_by_id(404)

        user_repo.get_by_id.assert_called_once_with(404)


class TestUserUpdateInfo:
    def test_update_info_success(
        self, user_repo: MagicMock, user_service: UserService, fake_user: Mock
    ) -> None:
        fake_user.username = "new_username"
        fake_user.first_name = "new_first_name"
        fake_user.last_name = "new_last_name"
        user_repo.update_by_id.return_value = fake_user
        update_data = UserUpdate(
            username="new_username",
            first_name="new_first_name",
            last_name="new_last_name",
        )

        result = user_service.update_info(1, update_data)

        assert isinstance(result, User)
        assert result.username == "new_username"
        assert result.first_name == "new_first_name"
        assert result.last_name == "new_last_name"

        user_repo.commit.assert_called_once()

    def test_update_info_not_found(
        self,
        user_repo: MagicMock,
        user_service: UserService,
    ) -> None:
        user_repo.update_by_id.return_value = None
        update_data = UserUpdate(username="new_username")

        with pytest.raises(NotFoundError, match="not found"):
            result = user_service.update_info(404, update_data)
        user_repo.update_by_id.assert_called_once_with(
            404, {"username": "new_username"}
        )
        user_repo.commit.assert_not_called()

    def test_update_info_empty_data(
        self,
        user_repo: MagicMock,
        user_service: UserService,
        fake_user: Mock,
    ) -> None:
        """Порожнє оновлення → викликає get_by_id."""
        user_repo.get_by_id.return_value = fake_user
        update_data = UserUpdate()

        result = user_service.update_info(1, update_data)

        assert isinstance(result, User)
        user_repo.get_by_id.assert_called_once_with(1)
        user_repo.update_by_id.assert_not_called()
