from fastapi import Depends
from backend.core.database import get_session
from backend.project_label.repository import ProjectLabelRepository


def get_project_label_rep(session=Depends(get_session)):
    return ProjectLabelRepository(session)


