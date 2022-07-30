from fastapi import APIRouter, Body, Depends, HTTPException, status

from backend.core.dependencies import get_pagination
from backend.core.schemas import HTTPError, ListPydantic, PaginationPydantic
from backend.project.dependencies import get_project_rep
from backend.project.repository import ProjectRepository
from backend.project_label.dependencies import get_project_label_rep
from backend.project_label.repository import ProjectLabelRepository
from backend.project_label.schemas import (
    ProjectLabelInCreatePydantic,
    ProjectLabelInUpdatePydantic,
    ProjectLabelPydantic,
)
from backend.user.dependencies import get_current_user

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

responses_project_label_not_found = {
    404: {
        "model": HTTPError,
        "content": {
            "application/json": {
                "examples": {
                    "project label not found": {
                        "value": {"detail": "Project label not found"}
                    },
                }
            }
        },
    }
}


@router.post(
    "/",
    response_model=ProjectLabelPydantic,
    responses=responses_project_not_exist,  # type: ignore
)
async def create_project_label(
    obj_in: ProjectLabelInCreatePydantic = Body(...),
    project_id: int = Body(...),
    project_label_rep: ProjectLabelRepository = Depends(get_project_label_rep),
    project_rep: ProjectRepository = Depends(get_project_rep),
    _=Depends(get_current_user),
):
    project = await project_rep.get_by_id(project_id)
    if not project:
        raise HTTPException(
            detail="Project not exist", status_code=status.HTTP_409_CONFLICT
        )
    return await project_label_rep.create(obj_in, project_id=project_id)


@router.get(
    "/",
    response_model=ListPydantic[ProjectLabelPydantic],
    responses=responses_project_not_exist,  # type: ignore
)
async def get_project_labels(
    project_id: int,
    project_label_rep: ProjectLabelRepository = Depends(get_project_label_rep),
    project_rep: ProjectRepository = Depends(get_project_rep),
    pagination: PaginationPydantic = Depends(get_pagination),
    _=Depends(get_current_user),
):
    project = await project_rep.get_by_id(project_id)
    if not project:
        raise HTTPException(
            detail="Project not exist", status_code=status.HTTP_409_CONFLICT
        )
    return ListPydantic(  # type: ignore
        items=await project_label_rep.get_multi(project_id, pagination)
    )


@router.get(
    "/{id}",
    response_model=ProjectLabelPydantic,
    responses=responses_project_label_not_found,  # type: ignore
)
async def get_project_label(
    id: int,
    project_label_rep: ProjectLabelRepository = Depends(get_project_label_rep),
    _=Depends(get_current_user),
):
    project_label = await project_label_rep.get_by_id(id)
    if not project_label:
        raise HTTPException(
            detail="Project label not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return project_label


@router.put(
    "/{id}",
    response_model=ProjectLabelPydantic,
    responses=responses_project_label_not_found,  # type: ignore
)
async def put_project_label(
    id: int,
    obj_in: ProjectLabelInUpdatePydantic,
    project_label_rep: ProjectLabelRepository = Depends(get_project_label_rep),
    _=Depends(get_current_user),
):
    project_label = await project_label_rep.get_by_id(id)
    if not project_label:
        raise HTTPException(
            detail="Project label not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    return await project_label_rep.update(project_label, obj_in)


@router.delete(
    "/{id}",
    response_model=ProjectLabelPydantic,
    responses=responses_project_label_not_found,  # type: ignore
)
async def delete_project_label(
    id: int,
    project_label_rep: ProjectLabelRepository = Depends(get_project_label_rep),
    _=Depends(get_current_user),
):
    project_label = await project_label_rep.get_by_id(id)
    if not project_label:
        raise HTTPException(
            detail="Project label not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return await project_label_rep.delete_by_id(id)
