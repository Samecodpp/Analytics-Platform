from pwdlib import PasswordHash

from ...domain.value_objects import Password
from ...domain.interfaces import IPasswordHasher


class PwdHasher(IPasswordHasher):
    def __init__(self):
        self._hasher = PasswordHash.recommended()

    def hash(self, password: Password) -> str:
        return self._hasher.hash(password.value)

    def verify(self, password: Password, hashed: str) -> bool:
        return self._hasher.verify(password.value, hashed)
