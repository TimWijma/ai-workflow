from typing import Optional, Dict
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid
import re

from app.schemas import step as step_schema
from app.crud import crud_step
from app.db.session import get_db

router = APIRouter()


@router.post("/flows/{flow_id}/steps", response_model=step_schema.Step)
def create_step_for_flow(flow_id: uuid.UUID, step: step_schema.StepCreate, db: Session = Depends(get_db)):
    step.flow_id = flow_id
    step.mappings = create_mappings(step)
    return crud_step.create_step(db=db, step=step)


@router.put("/steps/{step_id}", response_model=step_schema.Step)
def update_step(step_id: uuid.UUID, step: step_schema.StepUpdate, db: Session = Depends(get_db)):
    step.mappings = create_mappings(step)
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


def create_mappings(step: step_schema.StepBase) -> Optional[Dict[str, str]]:
    if not step:
        return None
    
    if step.type == "llm_call":
        if not step.config.get("prompt"):
            return None
        prompt_mappings = parse_mapping_str(step.config["prompt"])
        if not prompt_mappings:
            return None
        
        return prompt_mappings

def parse_mapping_str(input: str) -> Optional[Dict[str, str]]:
    if not input:
        return None

    MAPPING_PATTERN = re.compile(
        r"\{\{([0-9a-fA-F-]{36})\.([a-zA-Z0-9_]+)\}\}"
    )

    matches = MAPPING_PATTERN.findall(input)
    return [
        {
            "source_node": node_id,
            "field": field,
        }
        for node_id, field in matches
    ]
