from pydantic import BaseModel
import uuid
from datetime import datetime
from typing import List, Optional

from .step import Step

class FlowBase(BaseModel):
    name: str
    description: Optional[str] = None

class FlowCreate(FlowBase):
    pass

class FlowUpdate(FlowBase):
    pass

class FlowInDBBase(FlowBase):
    id: uuid.UUID
    created_at: datetime

    class Config:
        from_attributes = True

class Flow(FlowInDBBase):
    steps: List[Step] = []

class FlowInDB(FlowInDBBase):
    pass
