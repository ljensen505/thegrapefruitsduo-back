from fastapi import APIRouter, HTTPException, UploadFile, status

from app.admin import uploader
from app.db import QueryException, queries
from app.models import Musician

router = APIRouter(
    prefix="/musicians",
    tags=["musicians"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", status_code=status.HTTP_200_OK)
async def get_musicians() -> list[Musician]:
    try:
        return queries.get_musicians()
    except QueryException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_musician(id: int) -> Musician:
    try:
        musician = queries.get_musician(id)
        if musician is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return musician
    except QueryException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.post("/{id}/headshot", status_code=status.HTTP_200_OK)
async def update_musician_headshot(id: int, file: UploadFile) -> Musician | None:
    """Recieves a headshot image file, uploads it to cloudinary, and updates the musician's headshot url in the database"""
    return await update_headshot(id, file)


async def update_headshot(id: int, file: UploadFile) -> Musician:
    musician = queries.get_musician(id)

    if musician is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    prev_headshot_id = musician.headshot_id

    image_file = await file.read()
    data = uploader.upload(image_file)
    public_id = data.get("public_id")

    if public_id is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to upload image",
        )

    if prev_headshot_id not in ["margarite_copy_a4oxty", "coco_copy_jywbxm"]:
        try:
            uploader.destroy(prev_headshot_id)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to delete previous image: {e}",
            )

    try:
        queries.update_musician_headshot(id, public_id)
    except QueryException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )

    return await get_musician(id)
