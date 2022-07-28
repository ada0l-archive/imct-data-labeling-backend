from pydantic import BaseModel

from backend.core.schemas import ListPydantic


class LabelingProgressPydantic(BaseModel):
    labeled: int
    unlabeled: int
    labeled_percent: int


class LabelsInDashboard(BaseModel):
    name: str
    type: str
    count: int


class DashboardPydantic(BaseModel):
    labeling_progress: LabelingProgressPydantic
    labels: ListPydantic[LabelsInDashboard]
