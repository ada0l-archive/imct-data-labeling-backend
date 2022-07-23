from typing import Type

from backend.invite import schemas, models
from backend.core.repository import BaseRepository


class InviteRepository(
    BaseRepository[
        models.Invite,
        schemas.InvitePydantic,
        schemas.InviteInCreatePydantic,
        schemas.InviteInUpdatePydantic
    ]
):

    @property
    def _model(self) -> Type[models.Invite]:
        return models.Invite

    async def get_by_email(self, email: str) -> models.Invite:
        q = await self.session.execute(
            self
            .get_query()
            .filter(models.Invite.email == email)  # type: ignore
        )
        return q.scalars().first()
