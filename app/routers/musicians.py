from fastapi import APIRouter, HTTPException, Security, UploadFile, status

from app.admin.images import uploader
from app.admin.utils import VerifyToken
from app.controllers import Controller
from app.models.musician import Musician

router = APIRouter(
    prefix="/musicians",
    tags=["musicians"],
    responses={404: {"description": "Not found"}},
)

auth = VerifyToken()
controller = Controller()


@router.get("/", status_code=status.HTTP_200_OK)
async def get_musicians() -> list[Musician]:
    return await controller.get_musicians()


@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_musician(id: int) -> Musician:
    return await controller.get_musician(id)


@router.patch("/{id}")
async def update_musician(
    id: int, musician: Musician, auth_result=Security(auth.verify)
) -> Musician:
    """Updates a musician's bio, but requires the entire musician object to be sent in the request body.
    Requires authentication."""
    user_id: str = auth_result.get("sub")
    return await controller.update_musician(musician, user_id, id)


@router.post("/{id}/headshot", status_code=status.HTTP_200_OK)
async def update_musician_headshot(
    id: int, file: UploadFile, auth_result=Security(auth.verify)
) -> Musician | None:
    """Recieves a headshot image file, uploads it to cloudinary, and updates the musician's headshot url in the database"""
    user_id: str = auth_result.get("sub")
    musician = await controller.get_musician(id)
    return await controller.update_musician(musician, user_id, id, file=file)
