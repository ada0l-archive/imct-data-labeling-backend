from fastapi import APIRouter, Depends

from backend.core.schemas import ListPydantic
from backend.dashboard.schemas import (
    DashboardPydantic,
    LabelingProgressPydantic,
)
from backend.label.dependencies import get_label_rep
from backend.label.repository import LabelRepository
from backend.user.dependencies import get_current_user

router = APIRouter()


@router.get("/", response_model=DashboardPydantic)
async def get_dashboard(
    project_id: int,
    label_rep: LabelRepository = Depends(get_label_rep),
    _=Depends(get_current_user),
):
    labeling_progress = await label_rep.get_labeling_progress(project_id)
    labels = await label_rep.get_labels_with_count(project_id)
    return DashboardPydantic(
        labeling_progress=LabelingProgressPydantic(**labeling_progress),
        labels=ListPydantic(items=labels),  # type: ignore
    )
