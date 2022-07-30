from core.database import get_session
from fastapi import Depends
from image.repository import ImageRepository


def get_image_rep(session=Depends(get_session)):
    return ImageRepository(session)
