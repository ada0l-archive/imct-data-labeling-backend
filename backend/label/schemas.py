from pydantic import BaseModel


def get_label_scheme_by_type(type: str):
    return {
        'simple': SimpleLabel,
        'rectangle': RectangleLabel,
        'polygon': PolygonLabel,
    }[type]


class SimpleLabel(BaseModel):
    pass


class RectangleLabel(BaseModel):
    x: int
    y: int
    width: int
    height: int


class PolygonLabel(BaseModel):
    x: list[int]
    y: list[int]


class LabelBasePydantic(BaseModel):
    project_label_id: int
    image_id: int
    data: dict


class LabelPydantic(LabelBasePydantic):
    id: int
    creator_id: int

    class Config:
        orm_mode = True


class LabelInCreatePydantic(LabelBasePydantic):
    pass


class LabelInUpdatePydantic(BaseModel):
    data: dict
