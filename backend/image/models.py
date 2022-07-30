from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from backend.core.database import Base
from backend.dataset.models import Dataset
from backend.user.models import User


class Image(Base):
    id = Column(Integer, primary_key=True)
    uuid = Column(String, nullable=False)
    dataset_id = Column(
        Integer, ForeignKey(Dataset.id, ondelete="CASCADE"), nullable=True
    )
    dataset = relationship("Dataset")
    creator_id = Column(
        Integer, ForeignKey(User.id, ondelete="CASCADE"), nullable=True
    )
    creator = relationship("User")
