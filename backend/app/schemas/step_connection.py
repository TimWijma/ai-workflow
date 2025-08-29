from pydantic import BaseModel
import uuid

class StepConnectionBase(BaseModel):
    from_step_id: uuid.UUID
    to_step_id: uuid.UUID

class StepConnectionCreate(StepConnectionBase):
    pass

class StepConnectionInDBBase(StepConnectionBase):
    id: uuid.UUID

    class Config:
        from_attributes = True

class StepConnection(StepConnectionInDBBase):
    pass
