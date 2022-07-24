from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from backend.core.dependencies import get_pagination
from backend.core.schemas import HTTPError, ListPydantic, PaginationPydantic
from backend.project.dependencies import get_project_rep

from backend.project.repository import ProjectRepository
from backend.project.schemas import ProjectPydantic
from backend.user.dependencies import get_user_azure

router = APIRouter()


@router.get(
    "/{id}",
    response_model=ProjectPydantic,
    responses={
        404: {
            "model": HTTPError,
            "content": {
                "application/json": {
                    "examples": {
                        "not found": {
                            "value": {
                                "detail": "Project is not found"
                            }
                        },
                    }
                }
            }
        }
    },
)
async def get_project(
    id: int,
    project_rep: ProjectRepository = Depends(get_project_rep),
    _=Depends(get_user_azure)
):
    project = await project_rep.get_by_id(id)
    if not project:
        raise HTTPException(
            detail="Project is not found",
            status_code=status.HTTP_404_NOT_FOUND
        )
    return project


@router.get(
    "/",
    response_model=ListPydantic[ProjectPydantic],
)
async def get_projects(
    pagination: PaginationPydantic = Depends(get_pagination),
    project_rep: ProjectRepository = Depends(get_project_rep),
    _=Depends(get_user_azure)
):
    projects = await project_rep.get_multi(pagination)
    return ListPydantic( # type: ignore
        items=projects,
    )
