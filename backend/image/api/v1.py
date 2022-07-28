from uuid import uuid4
from fastapi import APIRouter, Body, Depends, HTTPException, UploadFile, status
from core.localstack import upload_image
from core.schemas import HTTPError, ListPydantic
from image.schemas import ImageInCreatePydantic, ImagePydantic
from core.dependencies import get_pagination
from core.schemas import PaginationPydantic
from dataset.dependencies import get_dataset_rep
from dataset.repository import DatasetRepository
from image.dependencies import get_image_rep
from image.repository import ImageRepository
from project.dependencies import get_project_rep

from project.repository import ProjectRepository
from user.dependencies import get_current_user

router = APIRouter()


responses_image_not_found={
    404: {
        "model": HTTPError,
        "content": {
            "application/json": {
                "examples": {
                    "not found": {
                        "value": {
                            "detail": "Image does not found"
                        }
                    },
                }
            }
        }
    }
}

example_project_not_exist ={
    "project does not exist": {
        "value": {
            "detail": "Project does not exist"
        }
    },
}

example_dataset_not_exist ={
    "dataset does not exist": {
        "value": {
            "detail": "Dataset does not exist"
        }
    },
}

@router.get(
    "/",
    response_model=ListPydantic,
    responses={
        409: {
            "model": HTTPError,
            "content": {
                "application/json": {
                    "examples": {
                        **example_project_not_exist,
                        **example_dataset_not_exist
                    }
                }
            }
        }
    }
)
async def get_images(
    project_id: int | None = None,
    dataset_id: int | None = None,
    image_rep: ImageRepository = Depends(get_image_rep),
    project_rep: ProjectRepository = Depends(get_project_rep),
    dataset_rep: DatasetRepository = Depends(get_dataset_rep),
    pagination: PaginationPydantic = Depends(get_pagination),
    _=Depends(get_current_user)
):
    if project_id is not None:
        project = await project_rep.get_by_id(dataset_id) # type: ignore
        if not project:
            raise HTTPException(
                detail="Dataset does not exist",
                status_code=status.HTTP_409_CONFLICT
            )
    if project_id is not None:
        dataset = await dataset_rep.get_by_id(dataset_id) # type: ignore
        if not dataset:
            raise HTTPException(
                detail="Dataset does not exist",
                status_code=status.HTTP_409_CONFLICT
            )
    images = await image_rep.get_multi(project_id=project_id,
                                       dataset_id=dataset_id,
                                       pagination=pagination)
    return ListPydantic( # type: ignore
        items=images
    )


@router.get(
    "/{id}",
    response_model=ImagePydantic
)
async def get_image(
    id: int,
    image_rep: ImageRepository = Depends(get_image_rep),
    _=Depends(get_current_user)
):
    image = await image_rep.get_by_id(id)
    return image


@router.post(
    "/",
    response_model=ListPydantic[ImagePydantic],
    responses={
        409: {
            "model": HTTPError,
            "content": {
                "application/json": {
                    "examples": {
                        **example_project_not_exist,
                        **example_dataset_not_exist
                    }
                }
            }
        }
    }
)
async def create_image(
    files: list[UploadFile],
    dataset_id: int = Body(...),
    image_rep: ImageRepository = Depends(get_image_rep),
    dataset_rep: DatasetRepository = Depends(get_dataset_rep),
    user=Depends(get_current_user)
):
    dataset = await dataset_rep.get_by_id(dataset_id)
    if not dataset:
        raise HTTPException(
            detail="Dataset does not exist",
            status_code=status.HTTP_409_CONFLICT
        )

    images_in_db = []
    for file in files:
        image_name = str(uuid4())
        await upload_image(file, f"{image_name}.png")
        images_in_db.append(
            await image_rep.create(ImageInCreatePydantic(uuid=image_name,
                                                         dataset_id=dataset_id,
                                                         creator_id=user.id)))
    return ListPydantic( # type: ignore
        items=images_in_db
    )
