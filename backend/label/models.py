from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB

from backend.core.database import Base
from backend.image.models import Image
from backend.project_label.models import ProjectLabel
from backend.user.models import User


class Label(Base):
    id = Column(Integer, primary_key=True)
    project_label_id = Column(Integer,
                              ForeignKey(ProjectLabel.id, ondelete="CASCADE"),
                              nullable=True)
    project_label = relationship("ProjectLabel")
    image_id = Column(Integer,
                      ForeignKey(Image.id, ondelete="CASCADE"),
                      nullable=True)
    image = relationship("Image")
    creator_id = Column(Integer,
                        ForeignKey(User.id, ondelete="CASCADE"),
                        nullable=True)
    creator = relationship("User")
    data = Column(JSONB,
                  nullable=False)
