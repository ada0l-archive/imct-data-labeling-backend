from fastapi import Depends
from backend.core.database import get_session
from backend.label.repository import LabelRepository


def get_label_rep(session=Depends(get_session)):
    return LabelRepository(session)


