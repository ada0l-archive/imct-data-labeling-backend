from fastapi import APIRouter, Depends

from backend.core.schemas import ListPydantic
from backend.project_label_type.models import LabelType
from backend.user.dependencies import get_current_user

router = APIRouter()


@router.get("/", response_model=ListPydantic[dict])
async def get_project_label_type(_=Depends(get_current_user)):
    return ListPydantic(  # type: ignore
        items=list(
            map(lambda item: {"name": item.name, "id": item.value}, LabelType)
        )
    )
