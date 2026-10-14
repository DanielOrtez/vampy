class InvalidCredentials(Exception):
    @property
    def detail(self) -> str:
        return "Invalid credentials."
