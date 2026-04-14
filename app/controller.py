import requests

from model import ProviderPriority, CreateRequestBody

BASE_URL = "http://localhost:3001"

async def call_provider(notification:CreateRequestBody, priority : ProviderPriority = "normal", trace_id: str = None):

    ENDPOINT = f"{BASE_URL}/v1/notify"

    headers = {
        "X-API-Key": "test-dev-2026"
    }

    params = {
        priority : str(priority),
        trace_id : trace_id # if it's None, requests lib will ignore it. 
    }

    response = requests.post(ENDPOINT,
                  headers=headers,
                  params=params,
                  json=notification.model_dump())
    
    print(f"CONTROLLER STATUS CODE:{response.status_code}")
    print(f"CONTROLLER TEXT:{response.text}")

    return response