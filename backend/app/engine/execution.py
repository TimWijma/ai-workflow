import os
from typing import Dict
from fastapi import HTTPException
from litellm import completion, acompletion
import uuid
import httpx
import asyncio
from sqlalchemy.orm import Session

from app.schemas import flow as flow_schema
from app.crud import crud_flow, crud_step

async def execute_flow(db: Session, flow_id: uuid.UUID) -> flow_schema.FlowResult:
    db_flow = crud_flow.get_flow(db, flow_id=flow_id)
    if db_flow is None:
        raise HTTPException(status_code=404, detail="Flow not found")

    results = []

    start_step_id = next((step.id for step in db_flow.steps if step.is_start), None)
    if not start_step_id:
        raise HTTPException(status_code=400, detail="No start step found")

    current_step = crud_step.get_step(db, start_step_id)

    step_variable_outputs: Dict[str, Dict[str, str]] = {}

    while current_step:
        step_variable_outputs[str(current_step.id)] = {}

        if current_step.type == "api_call":
            api_url = current_step.config.get("apiUrl")
            method = current_step.config.get("method", "GET")
            data = current_step.config.get("data", {})

            print(f"Calling API: {api_url} with method {method} and data {data}")

            if not api_url:
                raise HTTPException(status_code=400, detail=f"Step {current_step.id} missing API URL")
            
            try:
                response = await call_api(api_url, method, data)
                print(f"API response for step {current_step.id}: {response}")
                results.append(response)

                for variable in current_step.variables:
                    if variable in response:
                        step_variable_outputs[str(current_step.id)][variable] = response[variable]

            except Exception as e:
                print(f"Error calling API for step {current_step.id}: {str(e)}")
                # For now it keeps going, once data passing is implemented, should stop on error
                error_response = {"error": str(e), "step_id": str(current_step.id)}
                results.append(error_response)
        elif current_step.type == "llm_call":
            prompt = current_step.config.get("prompt")
            model = current_step.config.get("model", "ollama/gemma3:270m")
            temperature = current_step.config.get("temperature", 0.7)

            mappings_to_replace: Dict[tuple[str, str], str] = {}
            for mapping in current_step.mappings:
                source_node = mapping.get("source_node")
                field = mapping.get("field")

                if source_node in step_variable_outputs:
                    if field in step_variable_outputs[source_node]:
                        mappings_to_replace[(source_node, field)] = step_variable_outputs[source_node][field]

            for (step_id, field), value in mappings_to_replace.items():
                prompt = prompt.replace(f"{{{{{step_id}.{field}}}}}", value)

            try:
                print(f"Calling LLM: {model} \n Prompt: {prompt} \n Temperature: {temperature}")

                response = await call_llm(prompt, model, temperature)
                print(f"LLM response for step {current_step.id}: {response}")
                results.append(response)
            except Exception as e:
                print(f"Error calling LLM for step {current_step.id}: {str(e)}")
                error_response = {"error": str(e), "step_id": str(current_step.id)}
                results.append(error_response)

        current_step = get_next_step(db, current_step)

    result = {
        "id": db_flow.id,
        "status": "success",
        "output": {"message": "Flow executed successfully", "data": results}
    }

    return result

def get_next_step(db: Session, current_step: flow_schema.Step) -> flow_schema.Step | None:
    if len(current_step.source_connections) == 0:
        return None

    next_step_id = current_step.source_connections[0].to_step_id

    return crud_step.get_step(db, next_step_id)

async def call_api(url: str, method: str = "GET", data: dict = None) -> dict:
    try:
        async with httpx.AsyncClient() as client:
            if method == "POST":
                response = await client.post(url, json=data)
            elif method == "PUT":
                response = await client.put(url, json=data)
            elif method == "DELETE":
                response = await client.delete(url)
            else:
                response = await client.get(url)

            if response.status_code != 200 and response.status_code != 201:
                error_detail = f"HTTP {response.status_code}: {response.text}"
                print(f"API call failed: {error_detail}")
                raise HTTPException(status_code=response.status_code, detail=error_detail)

            response_data = response.json()
            return response_data
    except httpx.RequestError as e:
        print(f"Request error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Request failed: {str(e)}")
    except Exception as e:
        print(f"Unexpected error in call_api: {str(e)}")
        raise

async def call_llm(prompt: str, model: str, temperature: float) -> dict:
    response = await acompletion(
        model=model,
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=temperature,
        api_base="http://localhost:11434" if model.startswith("ollama") else None
    )

    print(f"LLM response: {response}")

    return response.choices[0].message.content