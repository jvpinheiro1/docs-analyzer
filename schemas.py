from pydantic import BaseModel, HttpUrl


class RepositorioRequest(BaseModel):
    github_url: HttpUrl