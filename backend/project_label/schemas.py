from pydantic import BaseModel

from backend.project_label_type.models import LabelType


class ProjectLabelBasePydantic(BaseModel):
    title: str
    type: LabelType


class ProjectLabelPydantic(ProjectLabelBasePydantic):
    id: int
    project_id: int

    class Config:
        orm_mode = True


class ProjectLabelInCreatePydantic(ProjectLabelBasePydantic):
    pass


class ProjectLabelInUpdatePydantic(ProjectLabelBasePydantic):
    pass
