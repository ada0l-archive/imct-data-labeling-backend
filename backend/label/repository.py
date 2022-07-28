from typing import Type
from backend.core.schemas import PaginationPydantic

from backend.label import schemas, models
from backend.core.repository import BaseRepository


class LabelRepository(
    BaseRepository[
        models.Label,
        schemas.LabelPydantic,
        schemas.LabelInCreatePydantic,
        schemas.LabelInUpdatePydantic
    ]
):

    @property
    def _model(self) -> Type[models.Label]:
        return models.Label

    async def get_multi(
        self,
        image_id: int | None = None,
        pagination: PaginationPydantic | None = None
    ) -> list[models.Label]:
        stmt = self.get_query()
        if pagination:
            stmt = stmt.limit(pagination.limit).offset(pagination.offset)
        if image_id:
            stmt = stmt.\
                filter(self._model.image_id == image_id) # type: ignore
        q = await self.session.execute(stmt)
        return q.scalars().all()
