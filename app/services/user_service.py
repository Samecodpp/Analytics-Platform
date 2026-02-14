from ..repositories.users_repo import UserRepository
from ..schemas.user_schemas import UserUpdate, User
from ..core.exceptions import NotFoundError


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def get_by_id(self, user_id: int) -> User:
        with self.user_repo:
            user = self.user_repo.get_by_id(user_id)
        if not user:
            raise NotFoundError("User not found")
        return User.model_validate(user)

    def update_info(self, user_id: int, update_data: UserUpdate) -> User:
        fields = update_data.model_dump(exclude_unset=True)
        if not fields:
            return self.get_by_id(user_id)
        with self.user_repo:
            updated_user = self.user_repo.update_by_id(user_id, fields)
            if not updated_user:
                raise NotFoundError("User not found")
            self.user_repo.commit()
        return User.model_validate(updated_user)
