from fastapi import FastAPI, HTTPException,Depends, status, BackgroundTasks
from contextlib import asynccontextmanager
from sqlmodel import Session
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
def create_request(payload: m.CreateRequestBody, session: Session = Depends(db.get_session)):
    notification = m.Notification.model_validate(payload)
    session.add(notification)
    session.commit()
    session.refresh(notification)
    return m.CreateRequestResponse(id=notification.id)

@app.post(
    path="/v1/requests/{id}/process",
    status_code=status.HTTP_202_ACCEPTED,
    responses={
        202: {"description": "Accepted"}
    },
)
def process_request(id:str,  background_tasks: BackgroundTasks, session: Session = Depends(db.get_session)):
    notification = session.get(m.Notification,id)
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Request not found",
        )
    else:

        if notification.status in [m.RequestStatus.processing, m.RequestStatus.sent]:
            return {"detail": "Accepted"}

        notification.status = m.RequestStatus.processing
        session.add(notification)
        session.commit()

        background_tasks.add_task(send_to_provider_and_update_status, id)

        return {"detail": "Accepted"}


@app.get(
    path="/v1/requests/{id}",
    response_model=m.RequestStatusResponse,
    status_code=status.HTTP_200_OK,
)
def get_request_status(id:str, session: Session = Depends(db.get_session)):
    
    notification = session.get(m.Notification,id)
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Request not found",
        )
    else:
        status_response = m.RequestStatusResponse.model_validate(notification)
        return status_response
    
# region private func

def send_to_provider_and_update_status(id:str):
    with Session(db.engine) as session:
        notification = session.get(m.Notification, id)
        if not notification:
            return
        try:
            notification_for_provider = m.CreateRequestBody.model_validate(notification)
            c.call_provider(notification=notification_for_provider)
            notification.status = m.RequestStatus.sent
        except Exception as e:
            notification.status = m.RequestStatus.failed
        
        session.add(notification)
        session.commit()

# endregion