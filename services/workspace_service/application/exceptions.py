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


class ForbbidenError(BaseError):
    """Raised when a action is forbbiden."""
    pass
