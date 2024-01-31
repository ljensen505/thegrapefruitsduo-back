from fastapi import APIRouter, HTTPException, Security, UploadFile, status

from app.admin import VerifyToken, uploader
from app.db import QueryException, queries
from app.models import Musician

router = APIRouter(
    prefix="/musicians",
    tags=["musicians"],
    responses={404: {"description": "Not found"}},
)

auth = VerifyToken()


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


@router.patch("/{id}")
async def update_musician(
    id: int, musician: Musician, auth_result=Security(auth.verify)
) -> Musician | None:
    """Updates a musician's bio, but requires the entire musician object to be sent in the request body.
    Requires authentication."""
    received_user_id = auth_result.get("sub")
    users = queries.get_users()
    user_subs = [user.auth0_id for user in users]
    if not received_user_id or received_user_id not in user_subs:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not authorized to perform this action",
        )
    queries.update_musician_bio(id, musician.bio)
    return await get_musician(id)


@router.post("/{id}/headshot", status_code=status.HTTP_200_OK)
async def update_musician_headshot(
    id: int, file: UploadFile, auth_result=Security(auth.verify)
) -> Musician | None:
    """Recieves a headshot image file, uploads it to cloudinary, and updates the musician's headshot url in the database"""
    received_user_id = auth_result.get("sub")
    users = queries.get_users()
    user_subs = [user.auth0_id for user in users]
    if not received_user_id or received_user_id not in user_subs:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not authorized to perform this action",
        )
    return await update_headshot(id, file)


async def update_headshot(id: int, file: UploadFile) -> Musician:
    musician = queries.get_musician(id)

    if musician is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    allowed_file_types = ["image/jpeg", "image/png"]
    if file.content_type not in allowed_file_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type {file.content_type} not allowed. Allowed file types are {allowed_file_types}",
        )
    max_file_size = 1000000  # 1 MB
    image_file = await file.read()
    if len(image_file) > max_file_size:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File size {len(image_file)} bytes exceeds maximum of {max_file_size} bytes",
        )

    prev_headshot_id = musician.headshot_id

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
