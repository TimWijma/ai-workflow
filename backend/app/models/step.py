import uuid
from sqlalchemy import Column, String, DateTime, func, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
from ..db.base import Base

class Step(Base):
    __tablename__ = "steps"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    flow_id = Column(UUID(as_uuid=True), ForeignKey("flows.id"), nullable=False)
    type = Column(String, nullable=False)
    config = Column(JSONB, nullable=True)
    pos_x = Column(Float, default=0.0)
    pos_y = Column(Float, default=0.0)
    created_at = Column(DateTime, default=func.now())

    flow = relationship("Flow", back_populates="steps")
    source_connections = relationship("StepConnection", foreign_keys="[StepConnection.from_step_id]", back_populates="from_step", cascade="all, delete-orphan")
    target_connections = relationship("StepConnection", foreign_keys="[StepConnection.to_step_id]", back_populates="to_step", cascade="all, delete-orphan")
