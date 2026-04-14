from pydantic import BaseModel
from enum import Enum


# region Enums
class RequestType(str, Enum):
    email = "email"
    sms = "sms"
    push = "push"

class RequestStatus(str, Enum):
    queued = "queued"
    processing = "processing"
    sent = "sent"
    failed = "failed"
# endregion


# region DTOs
class CreateRequestBody(BaseModel):
    to: str
    message: str
    type: RequestType


class CreateRequestResponse(BaseModel):
    id: str

class RequestStatusResponse(BaseModel):
    id: str
    status: RequestStatus

# endregion