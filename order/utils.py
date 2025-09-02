import requests
from django.conf import settings
import json
import os

API_BASE_URL = "https://api-hermes.pathao.com"


def get_access_token():
    url = f"{API_BASE_URL}/aladdin/api/v1/issue-token"
    payload = {
        "client_id": os.getenv('Pathao_CLIENT_ID'),
        "client_secret": os.getenv('Pathao_CLIENT_SECRET'),
        "username": os.getenv('Pathao_USERNAME'),
        "password": os.getenv('Pathao_PASSWORD'),
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
        # print("Validation error:", json.dumps(response.json(), indent=2))
        return response.json()     
    
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


def create_steadfast_order(order_data):
    url = f"{os.getenv('SteadFastAPIBASEURL')}/create_order"
    headers = {
        "Content-Type": "application/json",
        "Api-Key": os.getenv('SteadFastApiKey'),
        "Secret-Key": os.getenv('SteadFastSecretKey'),
    }
    return requests.post(url, headers=headers, json=order_data)

