class AppError(Exception):
    """Base application error."""
    def __init__(self, message: str = "An error occurred"):
        self.message = message
        super().__init__(self.message)


class AlreadyExistsError(AppError):
    """Raised when trying to create a resource that already exists."""
    pass


class NotFoundError(AppError):
    """Raised when a resource is not found."""
    pass


class InvalidCredentialsError(AppError):
    """Raised when authentication credentials are invalid."""
    pass


class InvalidTokenError(AppError):
    """Raised when a token is missing or invalid."""
    pass
