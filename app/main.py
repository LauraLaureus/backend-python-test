from fastapi import FastAPI, Response, status
import model as m

app = FastAPI(title="Notification Service (Technical Test)")

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