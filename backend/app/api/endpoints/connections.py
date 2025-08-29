from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid

from app.schemas import step_connection as step_connection_schema
from app.crud import crud_step_connection
from app.db.session import get_db

router = APIRouter()

@router.post("/steps/connections", response_model=step_connection_schema.StepConnection)
def create_connection(connection: step_connection_schema.StepConnectionCreate, db: Session = Depends(get_db)):
    return crud_step_connection.create_step_connection(db=db, connection=connection)

@router.delete("/steps/connections/{connection_id}", response_model=step_connection_schema.StepConnection)
def delete_connection(connection_id: uuid.UUID, db: Session = Depends(get_db)):
    db_connection = crud_step_connection.delete_step_connection(db, connection_id=connection_id)
    if db_connection is None:
        raise HTTPException(status_code=404, detail="Connection not found")
    return db_connection