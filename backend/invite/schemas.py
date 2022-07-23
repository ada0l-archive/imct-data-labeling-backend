from pydantic import BaseModel


class InviteBasePydantic(BaseModel):
    email: str


class InvitePydantic(InviteBasePydantic):
    id: int

    class Config:
        orm_mode = True


class InviteInCreatePydantic(InviteBasePydantic):
    pass


class InviteInUpdatePydantic(InviteBasePydantic):
    pass
