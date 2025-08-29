from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid
from typing import List

from app.schemas import flow as flow_schema
from app.crud import crud_flow
from app.db.session import get_db

router = APIRouter()

@router.get("/", response_model=List[flow_schema.Flow])
def read_flows(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    flows = crud_flow.get_flows(db, skip=skip, limit=limit)
    return flows

@router.get("/{flow_id}", response_model=flow_schema.Flow)
def read_flow(flow_id: uuid.UUID, db: Session = Depends(get_db)):
    db_flow = crud_flow.get_flow(db, flow_id=flow_id)
    if db_flow is None:
        raise HTTPException(status_code=404, detail="Flow not found")
    return db_flow

@router.post("/", response_model=flow_schema.Flow)
def create_flow(flow: flow_schema.FlowCreate, db: Session = Depends(get_db)):
    return crud_flow.create_flow(db=db, flow=flow)

@router.put("/{flow_id}", response_model=flow_schema.Flow)
def update_flow(flow_id: uuid.UUID, flow: flow_schema.FlowUpdate, db: Session = Depends(get_db)):
    db_flow = crud_flow.update_flow(db, flow_id=flow_id, flow=flow)
    if db_flow is None:
        raise HTTPException(status_code=404, detail="Flow not found")
    return db_flow

@router.delete("/{flow_id}", response_model=flow_schema.Flow)
def delete_flow(flow_id: uuid.UUID, db: Session = Depends(get_db)):
    db_flow = crud_flow.delete_flow(db, flow_id=flow_id)
    if db_flow is None:
        raise HTTPException(status_code=404, detail="Flow not found")
    return db_flow