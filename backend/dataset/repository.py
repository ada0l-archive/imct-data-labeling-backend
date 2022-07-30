from typing import Type

from backend.core.repository import BaseRepository
from backend.core.schemas import PaginationPydantic
from backend.dataset import models, schemas


class DatasetRepository(
    BaseRepository[
        models.Dataset,
        schemas.DatasetPydantic,
        schemas.DatasetInCreatePydantic,
        schemas.DatasetInUpdatePydantic,
    ]
):
    @property
    def _model(self) -> Type[models.Dataset]:
        return models.Dataset

    async def get_multi(
        self,
        project_id: int | None = None,
        pagination: PaginationPydantic | None = None,
    ) -> list[models.Dataset]:
        stmt = self.get_query()
        if pagination:
            stmt = stmt.limit(pagination.limit).offset(pagination.offset)
        if project_id:
            stmt = stmt.filter(
                self._model.project_id == project_id
            )  # type: ignore
        q = await self.session.execute(stmt)
        return q.scalars().all()
