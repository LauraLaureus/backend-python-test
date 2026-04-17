import requests
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from model import ProviderPriority, CreateRequestBody

BASE_URL = "http://localhost:3001"
@retry(
    stop=stop_after_attempt(3),  # 3 intentos max
    wait=wait_exponential(multiplier=1, min=1, max=10),  # 1s, 2s, 4s backoff
    retry=retry_if_exception_type((requests.RequestException,)),  # Solo errores de red
)
def call_provider(notification:CreateRequestBody, priority : ProviderPriority = "normal", trace_id: str = None):
    """
    Performs a call to the notificatio system. 

    Args:
        notification: a CreateRequestBody with the "message","to","type" keys. 

    """

    ENDPOINT = f"{BASE_URL}/v1/notify"

    headers = {
        "X-API-Key": "test-dev-2026"
    }

    params = {
        "priority" : str(priority),
        "trace_id" : trace_id # if it's None, requests lib will ignore it. 
    }

    response = requests.post(ENDPOINT,
                  headers=headers,
                  params=params,
                  json=notification.model_dump(),
                  timeout=(3.0, 10.0), # 3 seconds for connection and 10 por read.
                  )

    response.raise_for_status()
    
    print(f"CONTROLLER STATUS CODE:{response.status_code}")
    print(f"CONTROLLER TEXT:{response.text}")

    return response