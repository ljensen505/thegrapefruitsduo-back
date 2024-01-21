from app.models import Musician, User


class QueryException(Exception):
    pass


def build_musician(data: dict) -> Musician:
    try:
        musician = Musician(
            id=data["id"],
            name=data["name"],
            bio=data["bio"],
            headshot_id=data["headshot_id"],
        )
    except Exception as e:
        raise QueryException(f"Failed to build musician: {e}")
    return musician


def build_user(data: dict) -> User:
    try:
        user = User(
            id=data["id"],
            auth0_id=data["auth0_id"],
            name=data["name"],
            email=data["email"],
        )
    except Exception as e:
        raise QueryException(f"Failed to build user: {e}")
    return user
