import uuid
from sqlalchemy import Column, ForeignKey, String, DateTime, func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
from ..db.base import Base

class StepRun(Base):
    __tablename__ = "step_runs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    flow_run_id = Column(UUID(as_uuid=True), ForeignKey("flow_runs.id"), nullable=False)
    step_id = Column(UUID(as_uuid=True), ForeignKey("steps.id"), nullable=False)
    status = Column(String, default="running")
    input_data = Column(JSONB, nullable=True)
    output_data = Column(JSONB, nullable=True)

    # relationships
    flow_run = relationship("FlowRun", back_populates="steps")
    step = relationship("Step")
