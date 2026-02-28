import hashlib
import secrets

from ...domain.interfaces import IApiKeysManager
from ...domain.entities import ApiKey


class ApiKeysManager(IApiKeysManager):

    PREFIX = "sk"
    PREFIX_DISPLAY_LEN = 8

    def generate_key(self) -> ApiKey:
        raw = f"{self.PREFIX}_{secrets.token_urlsafe(32)}"
        key_hash = hashlib.sha256(raw.encode()).hexdigest()
        key_prefix = raw[:self.PREFIX_DISPLAY_LEN]

        return ApiKey(
            project_id=None,
            created_by=None,
            key_raw=raw,
            key_hash=key_hash,
            key_prefix=key_prefix,
        )

    def revoke_key(self, key: ApiKey) -> ApiKey:
        key.is_active = False
        return key
