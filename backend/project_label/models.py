from sqlalchemy import Column, ForeignKey, Integer, String, Enum
from sqlalchemy.orm import relationship

from backend.core.database import Base
from backend.project_label_type.models import LabelType
from backend.project.models import Project


class ProjectLabel(Base):
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    type = Column(Enum(LabelType))
    project_id = Column(Integer,
                        ForeignKey(Project.id, ondelete="CASCADE"),
                        nullable=False)
    project = relationship("Project")
