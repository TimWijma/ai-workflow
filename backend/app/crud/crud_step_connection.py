from sqlalchemy.orm import Session
import uuid

from ..models.step_connection import StepConnection
from ..schemas.step_connection import StepConnectionCreate


def get_step_connection(db: Session, connection_id: uuid.UUID):
    return db.query(StepConnection).filter(StepConnection.id == connection_id).first()


def create_step_connection(db: Session, connection: StepConnectionCreate):
    db_connection = StepConnection(**connection.model_dump())
    db.add(db_connection)
    db.commit()
    db.refresh(db_connection)
    return db_connection


def delete_step_connection(db: Session, connection_id: uuid.UUID):
    db_connection = get_step_connection(db, connection_id)
    if db_connection:
        db.delete(db_connection)
        db.commit()
    return db_connection
