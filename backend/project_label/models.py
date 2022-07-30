from sqlalchemy import Column, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from backend.core.database import Base
from backend.project.models import Project
from backend.project_label_type.models import LabelType


class ProjectLabel(Base):
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    type = Column(Enum(LabelType))
    project_id = Column(
        Integer, ForeignKey(Project.id, ondelete="CASCADE"), nullable=False
    )
    project = relationship("Project")
