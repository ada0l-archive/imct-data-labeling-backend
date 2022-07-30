from typing import Type

from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.orm.strategy_options import subqueryload

from backend.core.repository import BaseRepository
from backend.core.schemas import PaginationPydantic
from backend.dataset.models import Dataset
from backend.image import models, schemas
from backend.label.models import Label


class ImageRepository(
    BaseRepository[
        models.Image,
        schemas.ImagePydantic,
        schemas.ImageInCreatePydantic,
        schemas.ImageInUpdatePydantic,
    ]
):
    @property
    def _model(self) -> Type[models.Image]:
        return models.Image

    def get_query(self):
        return select(self._model).options(  # type: ignore
            joinedload('dataset')
        )  # type: ignore

    async def get_multi(
        self,
        project_id: int | None = None,
        dataset_id: int | None = None,
        pagination: PaginationPydantic | None = None,
    ) -> list[models.Image]:
        stmt = self.get_query()
        if pagination:
            stmt = stmt.limit(pagination.limit).offset(pagination.offset)
        if project_id:
            stmt = stmt.filter(
                Dataset.project_id == project_id
            )  # type: ignore
        if dataset_id:
            stmt = stmt.filter(
                self._model.dataset_id == dataset_id
            )  # type: ignore
        q = await self.session.execute(stmt)
        return q.scalars().all()

    async def get_for_export(self, project_id: int | None = None):
        stmt = (
            select(models.Image) # type: ignore
            .options(selectinload(models.Image.labels).subqueryload(Label.project_label))
            .join(Dataset)
            .filter(Dataset.project_id == project_id)
        )
        q = await self.session.execute(stmt)
        return q.scalars().all()
