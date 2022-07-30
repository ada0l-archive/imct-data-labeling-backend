from fastapi import APIRouter, Body, Depends, HTTPException, status

from backend.core.dependencies import get_pagination
from backend.core.schemas import HTTPError, ListPydantic, PaginationPydantic
from backend.dataset.dependencies import get_dataset_rep
from backend.dataset.repository import DatasetRepository
from backend.dataset.schemas import (
    DatasetInCreatePydantic,
    DatasetInUpdatePydantic,
    DatasetPydantic,
)
from backend.project.dependencies import get_project_rep
from backend.project.repository import ProjectRepository
from backend.user.dependencies import get_current_user
from backend.user.models import User

router = APIRouter()

responses_project_not_exist = {
    409: {
        "model": HTTPError,
        "content": {
            "application/json": {
                "examples": {
                    "project not exist": {
                        "value": {"detail": "Project not exist"}
                    },
                }
            }
        },
    }
}

responses_dataset_not_found = {
    404: {
        "model": HTTPError,
        "content": {
            "application/json": {
                "examples": {
                    "project label not found": {
                        "value": {"detail": "Dataset not found"}
                    },
                }
            }
        },
    }
}


@router.post(
    "/",
    response_model=DatasetPydantic,
    responses={**responses_project_not_exist},
)
async def create_dataset(
    obj_in: DatasetInCreatePydantic,
    project_id: int = Body(...),
    project_rep: ProjectRepository = Depends(get_project_rep),
    dataset_rep: DatasetRepository = Depends(get_dataset_rep),
    user: User = Depends(get_current_user),
):
    project = await project_rep.get_by_id(project_id)
    if not project:
        raise HTTPException(
            detail="Project not exist", status_code=status.HTTP_409_CONFLICT
        )
    return await dataset_rep.create(
        obj_in, project_id=project_id, creator_id=user.id
    )


@router.get(
    "/{id}",
    response_model=DatasetPydantic,
    responses={**responses_dataset_not_found},
)
async def get_dataset(
    id: int,
    dataset_rep: DatasetRepository = Depends(get_dataset_rep),
    _=Depends(get_current_user),
):
    dataset = await dataset_rep.get_by_id(id)
    if not dataset:
        raise HTTPException(
            detail="Dataset label not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return dataset


@router.delete(
    "/{id}",
    response_model=DatasetPydantic,
    responses={**responses_dataset_not_found},
)
async def delete_dataset(
    id: int,
    dataset_rep: DatasetRepository = Depends(get_dataset_rep),
    _=Depends(get_current_user),
):
    dataset = await dataset_rep.get_by_id(id)
    if not dataset:
        raise HTTPException(
            detail="Dataset label not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return await dataset_rep.delete_by_id(id)


@router.get(
    "/",
    response_model=ListPydantic[DatasetPydantic],
    responses={**responses_dataset_not_found},
)
async def get_datasets(
    project_id: int,
    project_rep: ProjectRepository = Depends(get_project_rep),
    dataset_rep: DatasetRepository = Depends(get_dataset_rep),
    pagination: PaginationPydantic = Depends(get_pagination),
    _=Depends(get_current_user),
):
    project = await project_rep.get_by_id(project_id)
    if not project:
        raise HTTPException(
            detail="Project not exist", status_code=status.HTTP_409_CONFLICT
        )

    return ListPydantic(  # type: ignore
        items=await dataset_rep.get_multi(project_id, pagination)
    )


@router.put(
    "/{id}",
    response_model=DatasetPydantic,
    responses={**responses_dataset_not_found},
)
async def put_project_label(
    id: int,
    obj_in: DatasetInUpdatePydantic,
    dataset_rep: DatasetRepository = Depends(get_dataset_rep),
    _=Depends(get_current_user),
):
    dataset = await dataset_rep.get_by_id(id)
    if not dataset:
        raise HTTPException(
            detail="Dataset label not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    return await dataset_rep.update(dataset, obj_in)
