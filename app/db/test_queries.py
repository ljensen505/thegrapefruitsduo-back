from app.models import Group, Musician, User

from .queries import (
    get_group,
    get_musician,
    get_musicians,
    get_user,
    get_users,
    update_musician_bio,
)


def test_get_musician():
    musician = get_musician(1)
    assert isinstance(musician, Musician)
    assert isinstance(musician.id, int)
    assert isinstance(musician.name, str)
    assert len(musician.name) > 0
    assert isinstance(musician.bio, str)
    assert len(musician.bio) > 0
    assert isinstance(musician.headshot_id, str)
    assert len(musician.headshot_id) > 0


def test_get_nonexistent_musician():
    musician = get_musician(3)
    assert musician is None


def test_get_musicians():
    musicians = get_musicians()
    assert isinstance(musicians, list)
    assert len(musicians) == 2
    assert isinstance(musicians[0], Musician)
    assert isinstance(musicians[1], Musician)


def test_get_group():
    group = get_group()
    assert isinstance(group, Group)
    assert isinstance(group.id, int)
    assert isinstance(group.name, str)
    assert len(group.name) > 0
    assert group.id == 1


def test_get_users():
    users = get_users()
    assert isinstance(users, list)
    assert len(users) >= 3
    assert all(isinstance(user, User) for user in users)


def test_get_user():
    user = get_user(1)
    assert isinstance(user, User)
    assert isinstance(user.id, int)
    assert isinstance(user.email, str)
    assert len(user.email) > 0
    assert isinstance(user.name, str)
    assert len(user.name) > 0
    assert isinstance(user.auth0_id, str)
    assert len(user.auth0_id) > 0


def test_get_nonexistent_user():
    user = get_user(45)
    assert user is None


def test_update_musician_bio():
    musician = get_musician(1)
    assert isinstance(musician, Musician)
    assert isinstance(musician.id, int)
    old_bio = str(musician.bio)
    new_bio = "clever new bio for the musician"
    updated_musician = update_musician_bio(musician.id, new_bio)
    assert isinstance(updated_musician, Musician)
    assert updated_musician.bio == new_bio
    assert updated_musician.bio != old_bio

    # reset bio
    musician.bio = old_bio
    update_musician_bio(musician.id, old_bio)
    musician = get_musician(1)
    assert isinstance(musician, Musician)
    assert musician.bio == old_bio
