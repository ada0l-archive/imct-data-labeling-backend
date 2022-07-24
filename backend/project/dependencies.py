from fastapi import Depends
from backend.core.database import get_session
from backend.project.repository import ProjectRepository


def get_project_rep(session=Depends(get_session)):
    return ProjectRepository(session)


