from fastapi import HTTPException, UploadFile, status

from app.admin.images import uploader
from app.controllers.base_controller import BaseController
from app.db.events import EventQueries
from app.models.event import Event, InsertionEvent, NewEvent


class EventController(BaseController):
    def __init__(self) -> None:
        super().__init__()
        self.db: EventQueries = EventQueries()

    async def get_events(self) -> list[Event]:
        data = await self.db.get_all()
        try:
            return [Event(**e) for e in data]
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error creating event objects: {e}",
            )

    async def get_event(self, id: int) -> Event:
        if (data := await self.db.get_one(id)) is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Event not found"
            )
        try:
            return Event(**data)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error creating event object: {e}",
            )

    async def create_event(self, event: NewEvent) -> Event:
        poster_id = await self._upload_poster(event.poster)
        event_for_insertion = InsertionEvent(
            name=event.name,
            location=event.location,
            description=event.description,
            time=event.time,
            poster=poster_id,
        )
        inserted_id = await self.db.insert_one(event_for_insertion)
        return await self.get_event(inserted_id)

    async def _upload_poster(self, poster: UploadFile) -> str:
        image_file = await self.verify_image(poster)
        try:
            data = uploader.upload(image_file)
            return data.get("public_id")
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error uploading image: {e}",
            )

    async def delete_event(self, id: int) -> None:
        await self.get_event(id)
        await self.db.delete_one(id)
