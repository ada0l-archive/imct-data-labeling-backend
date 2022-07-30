from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from backend.core.database import Base
from backend.project.models import Project
from backend.user.models import User


class Dataset(Base):
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    project_id = Column(
        Integer, ForeignKey(Project.id, ondelete="CASCADE"), nullable=True
    )
    project = relationship("Project")
    creator_id = Column(
        Integer, ForeignKey(User.id, ondelete="CASCADE"), nullable=True
    )
    creator = relationship("User")
