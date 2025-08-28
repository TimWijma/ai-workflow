from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.session import SessionLocal
from app.models import models
from app.schemas import schemas
from app.engine.execution import execute_workflow

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/flows", response_model=schemas.Flow)
def create_flow(flow: schemas.FlowCreate, db: Session = Depends(get_db)):
    db_flow = models.Flow(name=flow.name, description=flow.description)
    db.add(db_flow)
    db.commit()
    db.refresh(db_flow)

    node_id_to_db_id = {}
    steps = []
    for i, step_data in enumerate(flow.steps):
        db_step = models.Step(
            flow_id=db_flow.id,
            type=step_data.type,
            config=step_data.config,
            pos_x=step_data.pos_x,
            pos_y=step_data.pos_y,
        )
        db.add(db_step)
        steps.append(db_step)
    db.commit()

    for i, db_step in enumerate(steps):
        db.refresh(db_step)
        # The frontend sends node ids as "node-0", "node-1", etc.
        # We map them to the actual database ids.
        node_id_to_db_id[f"node-{i}"] = db_step.id

    connections = []
    for conn_data in flow.connections:
        db_conn = models.StepConnection(
            from_step_id=node_id_to_db_id.get(f"node-{conn_data.from_step_id}"),
            to_step_id=node_id_to_db_id.get(f"node-{conn_data.to_step_id}"),
        )
        db.add(db_conn)
        connections.append(db_conn)
    db.commit()

    for db_conn in connections:
        db.refresh(db_conn)

    return db_flow

@router.get("/flows", response_model=List[schemas.Flow])
def read_flows(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    flows = db.query(models.Flow).offset(skip).limit(limit).all()
    return flows

@router.get("/flows/{flow_id}", response_model=schemas.Flow)
def read_flow(flow_id: int, db: Session = Depends(get_db)):
    db_flow = db.query(models.Flow).filter(models.Flow.id == flow_id).first()
    if db_flow is None:
        raise HTTPException(status_code=404, detail="Flow not found")
    return db_flow

@router.post("/flows/{flow_id}/run")
def run_flow(flow_id: int, db: Session = Depends(get_db)):
    db_flow = db.query(models.Flow).filter(models.Flow.id == flow_id).first()
    if db_flow is None:
        raise HTTPException(status_code=404, detail="Flow not found")

    steps = db.query(models.Step).filter(models.Step.flow_id == flow_id).all()
    
    # A simple topological sort would be needed for parallel execution
    # For now, we execute in the order of creation
    steps.sort(key=lambda x: x.id)

    try:
        result = execute_workflow(db_flow, steps)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))