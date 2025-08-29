import uuid
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from ..db.base import Base

class StepConnection(Base):
    __tablename__ = "step_connections"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    from_step_id = Column(UUID(as_uuid=True), ForeignKey("steps.id"), nullable=False)
    to_step_id = Column(UUID(as_uuid=True), ForeignKey("steps.id"), nullable=False)

    from_step = relationship("Step", foreign_keys=[from_step_id], back_populates="source_connections")
    to_step = relationship("Step", foreign_keys=[to_step_id], back_populates="target_connections")
