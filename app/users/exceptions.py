import uuid


class UserNotFoundError(Exception):
    def __init__(self, user_id: uuid.UUID):
        self.user_id = user_id

    @property
    def detail(self) -> str:
        return f"User {self.user_id} not found."


class EmailAlreadyExistsError(Exception):
    @property
    def detail(self) -> str:
        return "Email already registered."
