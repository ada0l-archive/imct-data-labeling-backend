from pydantic import BaseModel


class ProjectBasePydantic(BaseModel):
    title: str
    description: str


class ProjectPydantic(ProjectBasePydantic):
    id: int

    class Config:
        orm_mode = True


class ProjectInCreatePydantic(ProjectBasePydantic):
    pass


class ProjectInUpdatePydantic(ProjectBasePydantic):
    pass
