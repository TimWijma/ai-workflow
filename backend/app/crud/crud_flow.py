from sqlalchemy.orm import Session
import uuid

from ..models.flow import Flow
from ..schemas.flow import FlowCreate, FlowUpdate


def get_flow(db: Session, flow_id: uuid.UUID):
    return db.query(Flow).filter(Flow.id == flow_id).first()


def get_flows(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Flow).offset(skip).limit(limit).all()


def create_flow(db: Session, flow: FlowCreate):
    db_flow = Flow(**flow.model_dump())
    db.add(db_flow)
    db.commit()
    db.refresh(db_flow)
    return db_flow


def update_flow(db: Session, flow_id: uuid.UUID, flow: FlowUpdate):
    db_flow = get_flow(db, flow_id)
    if db_flow:
        update_data = flow.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_flow, key, value)
        db.commit()
        db.refresh(db_flow)
    return db_flow


def delete_flow(db: Session, flow_id: uuid.UUID):
    db_flow = get_flow(db, flow_id)
    if db_flow:
        db.delete(db_flow)
        db.commit()
    return db_flow
