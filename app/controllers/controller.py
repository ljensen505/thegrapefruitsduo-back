from fastapi import HTTPException, UploadFile, status
from icecream import ic

from app.controllers.events import EventController
from app.controllers.group import GroupController
from app.controllers.musicians import MusicianController
from app.controllers.users import UserController
from app.models.event import Event, NewEvent
from app.models.group import Group
from app.models.musician import Musician
from app.models.user import User


class Controller:
    def __init__(self) -> None:
        self.event_controller = EventController()
        self.musician_controller = MusicianController()
        self.user_controller = UserController()
        self.group_controller = GroupController()

    async def get_musicians(self) -> list[Musician]:
        return await self.musician_controller.get_musicians()

    async def get_musician(self, id: int) -> Musician:
        return await self.musician_controller.get_musician(id)

    async def update_musician(
        self,
        musician: Musician,
        user_id: str,
        url_param_id: int,
        file: UploadFile | None = None,
    ) -> Musician:
        if musician.id != url_param_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ID in URL does not match ID in request body",
            )
        await self.user_controller.get_user_by_auth0_id(user_id)
        return await self.musician_controller.update_musician(
            musician_id=musician.id,
            new_bio=musician.bio,
            file=file,
        )

    async def get_events(self) -> list[Event]:
        return await self.event_controller.get_events()

    async def get_event(self, id: int) -> Event:
        return await self.event_controller.get_event(id)

    async def create_event(self, event: NewEvent, auth0_id: str) -> Event:
        await self.user_controller.get_user_by_auth0_id(auth0_id)
        return await self.event_controller.create_event(event)

    async def delete_event(self, id: int, auth0_id: str) -> None:
        await self.user_controller.get_user_by_auth0_id(auth0_id)
        await self.event_controller.delete_event(id)

    async def get_users(self) -> list[User]:
        return await self.user_controller.get_users()

    async def get_user(self, id: int) -> User:
        return await self.user_controller.get_user_by_id(id)

    async def get_group(self) -> Group:
        return await self.group_controller.get_group()

    async def update_group_bio(self, bio: str, auth0_id: str) -> Group:
        await self.user_controller.get_user_by_auth0_id(auth0_id)
        return await self.group_controller.update_group_bio(bio)
