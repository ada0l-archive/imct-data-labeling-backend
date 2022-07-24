from typing import Type

from backend.project import schemas, models
from backend.core.repository import BaseRepository


class ProjectRepository(
    BaseRepository[
        models.Project,
        schemas.ProjectPydantic,
        schemas.ProjectInCreatePydantic,
        schemas.ProjectInUpdatePydantic
    ]
):

    @property
    def _model(self) -> Type[models.Project]:
        return models.Project
