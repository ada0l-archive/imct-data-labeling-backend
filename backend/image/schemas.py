from pydantic import BaseModel


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
