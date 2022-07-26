from fastapi import Depends
from backend.core.database import get_session
from backend.dataset.repository import DatasetRepository


def get_dataset_rep(session=Depends(get_session)):
    return DatasetRepository(session)


