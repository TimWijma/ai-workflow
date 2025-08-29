import uuid
from sqlalchemy import Column, String, DateTime, func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from ..db.base import Base

class Flow(Base):
    __tablename__ = "flows"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=func.now())

    steps = relationship("Step", back_populates="flow", cascade="all, delete-orphan")
