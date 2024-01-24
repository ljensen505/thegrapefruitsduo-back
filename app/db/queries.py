from app.models import GROUP_TABLE, MUSICIAN_TABLE, USER_TABLE, Group, Musician, User

from .builders import build_musician, build_user
from .conn import connect_db


def get_group() -> Group:
    query = f"SELECT * FROM {GROUP_TABLE}"
    db = connect_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute(query)
    data = cursor.fetchone()
    cursor.close()
    db.close()

    name = data["name"]  # type: ignore
    bio = data["bio"]  # type: ignore
    id = data["id"]  # type: ignore

    if not data:
        raise Exception("error retrieving group")

    group = Group(name=name, bio=bio, id=id)

    return group


def update_musician_bio(id: int, bio: str) -> Musician | None:
    """Update a musician's bio as represented in the database"""
    musician = get_musician(id)
    if musician is None:
        return None
    db = connect_db()
    cursor = db.cursor()
    query = f"UPDATE {MUSICIAN_TABLE} SET bio = %s WHERE id = %s"
    cursor.execute(query, (bio, id))
    db.commit()
    cursor.close()
    db.close()
    musician.bio = bio
    return musician


def update_group_bio(bio: str) -> Group | None:
    """Update the group bio as represented in the database"""
    group = get_group()
    if group is None:
        return None
    db = connect_db()
    cursor = db.cursor()
    query = f"UPDATE {GROUP_TABLE} SET bio = %s WHERE id = %s"
    cursor.execute(query, (bio, group.id))
    db.commit()
    cursor.close()
    db.close()
    return group


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
