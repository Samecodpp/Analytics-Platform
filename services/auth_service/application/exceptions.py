class BaseError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class AlreadyExistsError(BaseError):
    """Raised when trying to create a resource that already exists."""
    pass


class NotFoundError(BaseError):
    """Raised when a resource is not found."""
    pass


class InvalidCredentialsError(BaseError):
    """Raised when authentication credentials are invalid."""
    pass


class InvalidTokenError(BaseError):
    """Raised when a token is missing or invalid."""
    pass
