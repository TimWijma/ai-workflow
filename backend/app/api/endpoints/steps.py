from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid

from app.schemas import step as step_schema
from app.crud import crud_step
from app.db.session import get_db

router = APIRouter()

@router.post("/flows/{flow_id}/steps", response_model=step_schema.Step)
def create_step_for_flow(flow_id: uuid.UUID, step: step_schema.StepCreate, db: Session = Depends(get_db)):
    step.flow_id = flow_id
    return crud_step.create_step(db=db, step=step)

@router.put("/steps/{step_id}", response_model=step_schema.Step)
def update_step(step_id: uuid.UUID, step: step_schema.StepUpdate, db: Session = Depends(get_db)):
    db_step = crud_step.update_step(db, step_id=step_id, step=step)
    if db_step is None:
        raise HTTPException(status_code=404, detail="Step not found")
    return db_step

@router.delete("/steps/{step_id}", response_model=step_schema.Step)
def delete_step(step_id: uuid.UUID, db: Session = Depends(get_db)):
    db_step = crud_step.delete_step(db, step_id=step_id)
    if db_step is None:
        raise HTTPException(status_code=404, detail="Step not found")
    return db_step