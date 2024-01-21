from app.models import Musician, User

from .builders import build_musician, build_user
from .conn import connect_db

MUSICIAN_TABLE = "musicians"
USER_TABLE = "users"


def get_users() -> list[User]:
    query = f"SELECT * FROM {USER_TABLE}"
    db = connect_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute(query)
    data = cursor.fetchall()
    users = [build_user(d) for d in data]  # type: ignore
    cursor.close()
    db.close()
    return users


def get_user(id: int) -> User | None:
    query = f"SELECT * FROM {USER_TABLE} WHERE id = %s"
    db = connect_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute(query, (id,))
    data = cursor.fetchone()
    cursor.close()
    db.close()

    if not data:
        return None
    user = build_user(data)  # type: ignore

    return user


def get_musicians() -> list[Musician]:
    query = f"SELECT * FROM {MUSICIAN_TABLE}"
    db = connect_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute(query)
    data = cursor.fetchall()
    musicians = [build_musician(d) for d in data]  # type: ignore
    cursor.close()
    db.close()
    return musicians


def get_musician(id: int) -> Musician | None:
    query = f"SELECT * FROM {MUSICIAN_TABLE} WHERE id = %s"
    db = connect_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute(query, (id,))
    data = cursor.fetchone()
    cursor.close()
    db.close()

    if not data:
        return None
    musician = build_musician(data)  # type: ignore

    return musician


def update_musician_headshot(id: int, headshot_id: str) -> Musician | None:
    """Update a musician's headshot as represented in the database by a cloudinary url"""
    musician = get_musician(id)
    if musician is None:
        return None
    db = connect_db()
    cursor = db.cursor()
    query = f"UPDATE {MUSICIAN_TABLE} SET headshot_id = %s WHERE id = %s"
    cursor.execute(query, (headshot_id, id))
    db.commit()
    cursor.close()
    db.close()
    return musician
