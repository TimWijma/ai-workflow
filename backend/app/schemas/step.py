from pydantic import BaseModel
import uuid
from datetime import datetime
from typing import Optional, Dict, Any

from .step_connection import StepConnection

class StepBase(BaseModel):
    name: str = "New Step"
    type: str
    config: Optional[Dict[str, Any]] = None
    pos_x: float = 0.0
    pos_y: float = 0.0
    is_start: bool = False
    variables: Optional[list[str]] = None
    mappings: Optional[list[Dict[str, str]]] = None

class StepCreate(StepBase):
    flow_id: uuid.UUID

class StepUpdate(StepBase):
    pass

class StepInDBBase(StepBase):
    id: uuid.UUID
    flow_id: uuid.UUID
    created_at: datetime

    class Config:
        from_attributes = True

class Step(StepInDBBase):
    source_connections: list[StepConnection] = []
    target_connections: list[StepConnection] = []

class StepInDB(StepInDBBase):
    pass
