from pydantic import BaseModel


class DatasetBasePydantic(BaseModel):
    title: str
    description: str


class DatasetPydantic(DatasetBasePydantic):
    id: int

    class Config:
        orm_mode = True


class DatasetInCreatePydantic(DatasetBasePydantic):
    pass


class DatasetInUpdatePydantic(DatasetBasePydantic):
    pass
