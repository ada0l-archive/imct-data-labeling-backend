from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import ValidationError
from backend.core.dependencies import get_pagination

from backend.core.schemas import ListPydantic, PaginationPydantic
from backend.label.dependencies import get_label_rep
from backend.label.repository import LabelRepository
from backend.label.schemas import LabelInCreatePydantic, LabelInUpdatePydantic, LabelPydantic, get_label_scheme_by_type
from backend.project.dependencies import get_project_rep
from backend.project.repository import ProjectRepository
from backend.project_label.dependencies import get_project_label_rep
from backend.project_label.repository import ProjectLabelRepository
from backend.project_label_type.models import LabelType
from backend.user.dependencies import get_current_user

router = APIRouter()


def check_data_in_label(project_label, data):
    type_name = LabelType(project_label.type).name
    schema = get_label_scheme_by_type(type_name)
    try:
        schema(**data)
    except ValidationError as e:
        raise HTTPException(
            detail=e.errors(),
            status_code=status.HTTP_400_BAD_REQUEST
        )


@router.get(
    "/",
    response_model=ListPydantic[LabelPydantic]
)
async def get_labels(
    image_id: int | None = None,
    image_rep: ProjectRepository = Depends(get_project_rep),
    label_rep: LabelRepository = Depends(get_label_rep),
    pagination: PaginationPydantic = Depends(get_pagination),
    _=Depends(get_current_user)
):
    if image_id is not None:
        image = await image_rep.get_by_id(image_id) # type: ignore
        if not image:
            raise HTTPException(
                detail="Image does not exist",
                status_code=status.HTTP_409_CONFLICT
            )
    labels = await label_rep.get_multi(image_id=image_id,
                                       pagination=pagination)
    return ListPydantic( # type: ignore
        items=labels
    )


@router.post(
    "/",
    response_model=LabelPydantic
)
async def create_label(
    obj_in: LabelInCreatePydantic,
    project_label_rep: ProjectLabelRepository = Depends(get_project_label_rep),
    image_rep: ProjectRepository = Depends(get_project_rep),
    label_rep: LabelRepository = Depends(get_label_rep),
    user=Depends(get_current_user)
):
    image = await image_rep.get_by_id(obj_in.image_id) # type: ignore
    if not image:
        raise HTTPException(
            detail="Image does not exist",
            status_code=status.HTTP_409_CONFLICT
        )
    # TODO: check Dataset.project_id == ProjectLabel.project_id
    project_label = await project_label_rep.get_by_id(obj_in.project_label_id)
    if not project_label:
        raise HTTPException(
            detail="Project label does not exist",
            status_code=status.HTTP_409_CONFLICT
        )

    check_data_in_label(project_label, obj_in.data)

    label = await label_rep.create(obj_in, creator_id=user.id)
    return label


@router.put(
    "/",
    response_model=LabelPydantic
)
async def update_label(
    id: int,
    obj_in: LabelInUpdatePydantic,
    project_label_rep: ProjectLabelRepository = Depends(get_project_label_rep),
    label_rep: LabelRepository = Depends(get_label_rep),
    _=Depends(get_current_user)
):
    label = await label_rep.get_by_id(id)
    if not label:
        raise HTTPException(
            detail="Label does not found",
            status_code=status.HTTP_404_NOT_FOUND
        )
    project_label = await project_label_rep.get_by_id(label.project_label_id)

    check_data_in_label(project_label, obj_in.data)

    label = await label_rep.update(label, obj_in)
    return label


@router.get(
    "/{id}",
    response_model=LabelPydantic
)
async def get_label(
    id: int,
    label_rep: LabelRepository = Depends(get_label_rep),
    _=Depends(get_current_user)
):
    label = await label_rep.get_by_id(id)
    if not label:
        raise HTTPException(
            detail="Label does not found",
            status_code=status.HTTP_404_NOT_FOUND
        )
    return label
