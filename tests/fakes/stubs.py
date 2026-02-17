class StubTokenService:
    def create_access_token(self, user_id):
        return "access_stub"

    def create_refresh_token(self, user_id):
        return "refresh_stub"

    def verify_refresh_token(self, token):
        return {"sub": "1", "type": "refresh"}


class StubExpiredTokenService:
    def create_access_token(self, user_id):
        return "access_stub"

    def create_refresh_token(self, user_id):
        return "refresh_stub"

    def verify_refresh_token(self, token):
        raise ValueError("Refresh token expired")


class StubInvalidTokenService:
    def create_access_token(self, user_id):
        return "access_stub"

    def create_refresh_token(self, user_id):
        return "refresh_stub"

    def verify_refresh_token(self, token):
        raise ValueError("Invalid refresh token")
