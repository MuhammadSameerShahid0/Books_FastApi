from pydantic import BaseModel


class CreateAuthor(BaseModel):
    name: str
    email: str
    bio : str
    nationality: str