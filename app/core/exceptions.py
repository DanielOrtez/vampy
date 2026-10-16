class VAMException(Exception):
    status_code: int
    error: str
    detail: str | dict[str, str] | None = None

    def to_content(self):
        content = {"error": self.error}
        if self.detail:
            content["detail"] = self.detail

        return content
