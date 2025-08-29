from fastapi import HTTPException
from litellm import completion
import uuid
import httpx
import asyncio
from sqlalchemy.orm import Session

from app.schemas import flow as flow_schema
from app.crud import crud_flow

async def execute_flow(db: Session, flow_id: uuid.UUID) -> flow_schema.FlowResult:
    db_flow = crud_flow.get_flow(db, flow_id=flow_id)
    if db_flow is None:
        raise HTTPException(status_code=404, detail="Flow not found")

    results = []

    for step in db_flow.steps:
        if step.type == "api_call":
            api_url = step.config.get("apiUrl")
            method = step.config.get("method", "GET")
            data = step.config.get("data", {})

            print(f"Calling API: {api_url} with method {method} and data {data}")

            if not api_url:
                raise HTTPException(status_code=400, detail=f"Step {step.id} missing API URL")
            
            try:
                response = await call_api(api_url, method, data)
                print(f"API response for step {step.id}: {response}")
                results.append(response)
            except Exception as e:
                print(f"Error calling API for step {step.id}: {str(e)}")
                # You can choose to either raise the exception or continue with other steps
                # For now, let's continue and add the error to results
                error_response = {"error": str(e), "step_id": str(step.id)}
                results.append(error_response)

    result = {
        "id": db_flow.id,
        "status": "success",
        "output": {"message": "Flow executed successfully", "data": results}
    }

    return result

async def call_api(url: str, method: str = "GET", data: dict = None) -> dict:
    try:
        async with httpx.AsyncClient() as client:
            print(f"Making {method} request to {url}")
            if method == "POST":
                response = await client.post(url, json=data)
            else:
                response = await client.get(url)

            print(f"Response status: {response.status_code}")
            
            if response.status_code != 200 and response.status_code != 201:
                error_detail = f"HTTP {response.status_code}: {response.text}"
                print(f"API call failed: {error_detail}")
                raise HTTPException(status_code=response.status_code, detail=error_detail)

            response_data = response.json()
            print(f"Response data: {response_data}")
            return response_data
    except httpx.RequestError as e:
        print(f"Request error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Request failed: {str(e)}")
    except Exception as e:
        print(f"Unexpected error in call_api: {str(e)}")
        raise

async def call_llm(prompt: str, model: str, temperature: float) -> dict:
    response = await completion(
        model=model,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return response.json()