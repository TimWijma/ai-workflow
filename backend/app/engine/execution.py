from fastapi import HTTPException
import uuid
from requests import Session

from app.schemas import flow as flow_schema
from app.crud import crud_flow

def execute_flow(db: Session, flow_id: uuid.UUID) -> flow_schema.FlowResult:
    db_flow = crud_flow.get_flow(db, flow_id=flow_id)
    if db_flow is None:
        raise HTTPException(status_code=404, detail="Flow not found")

    results = []

    for step in db_flow.steps:
        if step.type == "api_call":
            api_url = step.config.get("apiUrl")
            method = step.config.get("method", "GET")
            data = step.config.get("data", {})
            if not api_url:
                raise HTTPException(status_code=400, detail=f"Step {step.id} missing API URL")
            response = call_api(api_url, method, data)

            results.append(response)

    result = {
        "id": db_flow.id,
        "status": "success",
        "output": {"message": "Flow executed successfully", "data": results}
    }

    return result

def call_api(url: str, method: str = "GET", data: dict = None) -> dict:
    with Session() as session:
        if method == "POST":
            response = session.post(url, json=data)
        else:
            response = session.get(url)

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)

        return response.json()