from fastapi import FastAPI, Response, status
from contextlib import asynccontextmanager
import model as m
import controller as c
import db

@asynccontextmanager
async def lifespan(app: FastAPI):
    db.create_db_and_tables()
    yield

app = FastAPI(title="Notification Service (Technical Test)", lifespan=lifespan)
# we don't have to do anything with the port since it's already config in the Dockerfile



@app.post(
    path="/v1/requests",
    response_model=m.CreateRequestResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_request(payload: m.CreateRequestBody):
    pass

@app.post(
    path="/v1/requests/{id}/process",
    responses={
        200: {"description": "OK"},
        202: {"description": "Accepted"}
    },
)
async def process_request(id:str,response:Response):
    pass

@app.get(
    path="/v1/requests/{id}",
    response_model=m.RequestStatusResponse,
    status_code=status.HTTP_200_OK,
)
async def get_request_status(id:str):
    pass