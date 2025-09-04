from sqlalchemy.orm import Session
import uuid

from ..models.step import Step
from ..schemas.step import StepCreate, StepUpdate


def get_step(db: Session, step_id: uuid.UUID):
    return db.query(Step).filter(Step.id == step_id).first()


def create_step(db: Session, step: StepCreate):
    db_step = Step(**step.model_dump())
    db.add(db_step)
    db.commit()
    db.refresh(db_step)
    return db_step


def update_step(db: Session, step_id: uuid.UUID, step: StepUpdate):
    db_step = get_step(db, step_id)
    if db_step:
        update_data = step.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_step, key, value)
        db.commit()
        db.refresh(db_step)
    return db_step


def delete_step(db: Session, step_id: uuid.UUID):
    db_step = get_step(db, step_id)
    if db_step:
        db.delete(db_step)
        db.commit()
    return db_step
