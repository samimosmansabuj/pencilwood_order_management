import requests
from django.conf import settings
import json

API_BASE_URL = "https://api-hermes.pathao.com"
CLIENT_ID = "ELe3Q94b69"
CLIENT_SECRET = "f0Al9C3TZggJLtCFiP20CEhjsMfkkE1bkNAsxhzL"
USERNAME = "pencilwoodbd@gmail.com"
PASSWORD = "Pathaopencilwood@1"


def get_access_token():
    url = f"{API_BASE_URL}/aladdin/api/v1/issue-token"
    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "username": USERNAME,
        "password": PASSWORD,
        "grant_type": "password",
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    token_data = response.json()
    # Store token_data['access_token'] and token_data['expires_in'] as needed
    return token_data['access_token']

def create_pathao_order(order_data, access_token):
    url = f"{API_BASE_URL}/aladdin/api/v1/orders"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    response = requests.post(url, headers=headers, json=order_data)

    if response.status_code == 422:
        print("Validation error:", json.dumps(response.json(), indent=2))
    
    response.raise_for_status()  # This will raise an error if status is 4xx or 5xx
    return response.json()


def get_order_info(consignment_id, access_token):
    url = f"{API_BASE_URL}/aladdin/api/v1/orders/{consignment_id}/info"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()



