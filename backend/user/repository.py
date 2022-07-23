from typing import Type

from backend.user import schemas, models
from backend.core.repository import BaseRepository


class UserRepository(
    BaseRepository[
        models.User,
        schemas.UserPydantic,
        schemas.UserAzure,
        schemas.UserInUpdatePydantic
    ]
):

    @property
    def _model(self) -> Type[models.User]:
        return models.User

    async def get_by_email(self, email: str) -> models.User:
        q = await self.session.execute(
            self
            .get_query()
            .filter(models.User.email == email)  # type: ignore
        )
        return q.scalars().first()

