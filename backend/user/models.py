from sqlalchemy import Column, Integer, String

from backend.core.database import Base


class User(Base):
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
