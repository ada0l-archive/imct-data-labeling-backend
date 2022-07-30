from typing import Type

from backend.core.repository import BaseRepository
from backend.core.schemas import PaginationPydantic
from backend.project_label import models, schemas


class ProjectLabelRepository(
    BaseRepository[
        models.ProjectLabel,
        schemas.ProjectLabelPydantic,
        schemas.ProjectLabelInCreatePydantic,
        schemas.ProjectLabelInUpdatePydantic,
    ]
):
    @property
    def _model(self) -> Type[models.ProjectLabel]:
        return models.ProjectLabel

    async def get_multi(
        self,
        project_id: int | None = None,
        pagination: PaginationPydantic | None = None,
    ) -> list[models.ProjectLabel]:
        stmt = self.get_query()
        if pagination:
            stmt = stmt.limit(pagination.limit).offset(pagination.offset)
        if project_id:
            stmt = stmt.filter(
                self._model.project_id == project_id
            )  # type: ignore
        q = await self.session.execute(stmt)
        return q.scalars().all()
