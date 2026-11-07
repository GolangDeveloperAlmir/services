"""Domain exceptions translated to stable HTTP error responses."""


class UserNotFoundError(Exception):
    """Raised when a requested profile does not exist."""

    def __init__(self) -> None:
        """Create the domain error with its stable public message."""
        super().__init__("User not found")


class EmailAlreadyExistsError(Exception):
    """Raised when a profile email is already owned by another user."""

    def __init__(self) -> None:
        """Create the domain error with its stable public message."""
        super().__init__("Email already exists")
