
import enum
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    JSON,
    Float,
    Enum,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()


class Flow(Base):
    __tablename__ = "flows"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    steps = relationship("Step", back_populates="flow", cascade="all, delete-orphan")
    executions = relationship("Execution", back_populates="flow")


class Step(Base):
    __tablename__ = "steps"
    id = Column(Integer, primary_key=True, index=True)
    flow_id = Column(Integer, ForeignKey("flows.id"))
    type = Column(String)
    config = Column(JSON)
    pos_x = Column(Float)
    pos_y = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    flow = relationship("Flow", back_populates="steps")
    source_connections = relationship(
        "StepConnection",
        foreign_keys="[StepConnection.from_step_id]",
        back_populates="source_step",
        cascade="all, delete-orphan",
    )
    target_connections = relationship(
        "StepConnection",
        foreign_keys="[StepConnection.to_step_id]",
        back_populates="target_step",
        cascade="all, delete-orphan",
    )


class StepConnection(Base):
    __tablename__ = "step_connections"
    id = Column(Integer, primary_key=True, index=True)
    from_step_id = Column(Integer, ForeignKey("steps.id"))
    to_step_id = Column(Integer, ForeignKey("steps.id"))
    source_step = relationship("Step", foreign_keys=[from_step_id], back_populates="source_connections")
    target_step = relationship("Step", foreign_keys=[to_step_id], back_populates="target_connections")


class ExecutionStatus(enum.Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class Execution(Base):
    __tablename__ = "executions"
    id = Column(Integer, primary_key=True, index=True)
    flow_id = Column(Integer, ForeignKey("flows.id"))
    status = Column(Enum(ExecutionStatus), default=ExecutionStatus.PENDING)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    finished_at = Column(DateTime(timezone=True), onupdate=func.now())
    logs = Column(JSON)
    flow = relationship("Flow", back_populates="executions")
    step_executions = relationship("StepExecution", back_populates="execution")


class StepExecution(Base):
    __tablename__ = "step_executions"
    id = Column(Integer, primary_key=True, index=True)
    execution_id = Column(Integer, ForeignKey("executions.id"))
    step_id = Column(Integer, ForeignKey("steps.id"))
    status = Column(Enum(ExecutionStatus), default=ExecutionStatus.PENDING)
    input = Column(JSON)
    output = Column(JSON)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    finished_at = Column(DateTime(timezone=True), onupdate=func.now())
    execution = relationship("Execution", back_populates="step_executions")
    step = relationship("Step")
