from fastapi import APIRouter, Depends
from backend.image.dependencies import get_image_rep
from backend.image.repository import ImageRepository
from backend.image.schemas import ImageWithLabelsPydantic
from backend.user.dependencies import get_current_user

router = APIRouter()


@router.get("/", response_model=list[ImageWithLabelsPydantic])
async def get_export(
    project_id: int,
    image_rep: ImageRepository = Depends(get_image_rep),
    _=Depends(get_current_user)
):
    images = await image_rep.get_for_export(project_id)
    return images
