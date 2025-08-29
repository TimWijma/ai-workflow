from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid
from litellm import completion

from app.crud import crud_step
from app.db.session import get_db

router = APIRouter()

@router.post("/steps/{step_id}/llm_call")
def llm_call(step_id: uuid.UUID, db: Session = Depends(get_db)):
    db_step = crud_step.get_step(db, step_id=step_id)
    if not db_step:
        raise HTTPException(status_code=404, detail="Step not found")

    if db_step.type != 'llm_call':
        raise HTTPException(status_code=400, detail="Step is not an LLM call step")

    prompt = db_step.config.get("prompt")
    if not prompt:
        raise HTTPException(status_code=400, detail="Prompt not found in step config")

    try:
        response = completion(model="gpt-3.5-turbo", messages=[{"content": prompt, "role": "user"}])
        return {"output": response.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))