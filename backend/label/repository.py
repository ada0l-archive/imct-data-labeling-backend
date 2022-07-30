from typing import Type

from sqlalchemy import func, select
from sqlalchemy.orm import joinedload, selectinload

from backend.core.repository import BaseRepository
from backend.core.schemas import PaginationPydantic
from backend.dataset.models import Dataset
from backend.image.models import Image
from backend.label import models, schemas
from backend.project_label.models import ProjectLabel
from backend.project_label_type.models import LabelType


class LabelRepository(
    BaseRepository[
        models.Label,
        schemas.LabelPydantic,
        schemas.LabelInCreatePydantic,
        schemas.LabelInUpdatePydantic,
    ]
):
    @property
    def _model(self) -> Type[models.Label]:
        return models.Label

    async def get_multi(
        self,
        image_id: int | None = None,
        pagination: PaginationPydantic | None = None,
    ) -> list[models.Label]:
        stmt = self.get_query()
        if pagination:
            stmt = stmt.limit(pagination.limit).offset(pagination.offset)
        if image_id:
            stmt = stmt.filter(
                self._model.image_id == image_id
            )  # type: ignore
        q = await self.session.execute(stmt)
        return q.scalars().all()

    async def get_labeling_progress(self, project_id: int) -> dict[str, int]:
        stmt = (
            select([func.count()])
            .select_from(Image)  # type: ignore
            .join(Dataset)  # type: ignore
            .where(Dataset.project_id == project_id)  # type: ignore
            .outerjoin(models.Label, models.Label.image_id == Image.id)
            .where(models.Label.id.is_(None))
        )
        q = await self.session.execute(stmt)
        unlabeled = q.scalars().first()
        stmt = (
            select([func.count()])
            .select_from(Image)  # type: ignore
            .join(Dataset)  # type: ignore
            .where(Dataset.project_id == project_id)  # type: ignore
        )
        q = await self.session.execute(stmt)
        all = q.scalars().first()
        return {
            "labeled": all - unlabeled,
            "unlabeled": unlabeled,
            "labeled_percent": round((all - unlabeled) / all * 100, 2),
        }

    async def get_labels_with_count(self, project_id: int):
        stmt = (
            select(
                [
                    ProjectLabel.title,
                    ProjectLabel.type,
                    func.count(models.Label.id),
                ]
            )
            .select_from(ProjectLabel)  # type: ignore
            .filter(ProjectLabel.project_id == project_id)  # type: ignore
            .join(models.Label)  # type: ignore
            .group_by(ProjectLabel.title, ProjectLabel.type)
        )
        q = await self.session.execute(stmt)
        result = []
        for row in q:
            result.append(
                {
                    "name": row[0],
                    "type": LabelType(row[1]).name,
                    "count": row[2],
                }
            )
        return result
