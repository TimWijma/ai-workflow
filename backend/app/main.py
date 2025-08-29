from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.endpoints import flows, steps, connections, llm

app = FastAPI()

# CORS
origins = [
    "http://localhost:5173",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(flows.router, prefix="/flows", tags=["flows"])
app.include_router(steps.router, tags=["steps"])
app.include_router(connections.router, tags=["connections"])
app.include_router(llm.router, tags=["llm"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Workflow Backend"}
