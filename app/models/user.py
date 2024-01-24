from pydantic import BaseModel


class User(BaseModel):
    auth0_id: str
    name: str
    email: str
    id: int | None = None


USER_TABLE = "users"
