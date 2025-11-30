from fastapi import FastAPI
from microservice_api.routes import kalex

app = FastAPI()

app.include_router(kalex.router)