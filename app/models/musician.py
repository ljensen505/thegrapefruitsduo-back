from pydantic import BaseModel


class Musician(BaseModel):
    name: str
    bio: str
    headshot_id: str
    id: int | None = None


MUSICIAN_TABLE = "musicians"
