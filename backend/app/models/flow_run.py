import uuid
from sqlalchemy import Column, ForeignKey, String, DateTime, func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from ..db.base import Base

class FlowRun(Base):
    __tablename__ = "flow_runs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    flow_id = Column(UUID(as_uuid=True), ForeignKey("flows.id"), nullable=False)

    created_at = Column(DateTime, default=func.now())

    flow = relationship("Flow", back_populates="runs", cascade="all, delete-orphan")
    steps = relationship("Step", back_populates="flow_run", cascade="all, delete-orphan")