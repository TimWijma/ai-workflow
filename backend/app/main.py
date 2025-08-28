from fastapi import FastAPI
from app.api.endpoints import flows
from app.db.session import engine
from app.models import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(flows.router, prefix="/api/v1")
