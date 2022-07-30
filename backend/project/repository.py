from typing import Type

from backend.core.repository import BaseRepository
from backend.project import models, schemas


class ProjectRepository(
    BaseRepository[
        models.Project,
        schemas.ProjectPydantic,
        schemas.ProjectInCreatePydantic,
        schemas.ProjectInUpdatePydantic,
    ]
):
    @property
    def _model(self) -> Type[models.Project]:
        return models.Project
