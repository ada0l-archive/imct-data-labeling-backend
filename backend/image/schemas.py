from typing import Any
from pydantic import BaseModel, root_validator, validator

from backend.project_label_type.models import LabelType


class ImageBasePydantic(BaseModel):
    uuid: str
    dataset_id: int
    creator_id: int


class ImagePydantic(ImageBasePydantic):
    id: int

    class Config:
        orm_mode = True


class ImageInCreatePydantic(ImageBasePydantic):
    pass


class ImageInUpdatePydantic(ImageBasePydantic):
    pass


class ProjectLabelInLabelInImagePydantic(BaseModel):
    type: str
    title: str


    @validator("type", pre=True)
    def set_value_from_enum(cls, v):
        return LabelType(v).name


    class Config:
        orm_mode = True


class LabelInImagePydantic(BaseModel):
    data: dict
    project_label: ProjectLabelInLabelInImagePydantic

    class Config:
        orm_mode = True


class ImageWithLabelsPydantic(BaseModel):
    uuid: str
    labels: list[LabelInImagePydantic]

    class Config:
        orm_mode = True



