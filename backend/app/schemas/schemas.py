
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

# Step Schemas
class StepBase(BaseModel):
    type: str
    config: Dict[str, Any]
    pos_x: float
    pos_y: float

class StepCreate(StepBase):
    pass

class Step(StepBase):
    id: int
    flow_id: int
    created_at: datetime

    class Config:
        orm_mode = True

# Step Connection Schemas
class StepConnectionBase(BaseModel):
    from_step_id: int
    to_step_id: int

class StepConnectionCreate(StepConnectionBase):
    pass

class StepConnection(StepConnectionBase):
    id: int

    class Config:
        orm_mode = True

# Flow Schemas
class FlowBase(BaseModel):
    name: str
    description: Optional[str] = None

class FlowCreate(FlowBase):
    steps: List[StepCreate] = []
    connections: List[StepConnectionCreate] = []

class Flow(FlowBase):
    id: int
    created_at: datetime
    steps: List[Step] = []
    connections: List[StepConnection] = []

    class Config:
        orm_mode = True

class FlowUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    steps: Optional[List[StepCreate]] = None
    connections: Optional[List[StepConnectionCreate]] = None
