import requests
from django.conf import settings
import json
import os
from django.utils.text import slugify
from account.models import SteadFastAPI

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


def create_steadfast_order(order_data, account):
    if SteadFastAPI.objects.filter(account=account).exists() and len(SteadFastAPI.objects.filter(account=account)) == 1:
        steadfast = SteadFastAPI.objects.get(account=account)
        url = f"{steadfast.base_url}/create_order"
        headers = {
            "Content-Type": "application/json",
            "Api-Key": steadfast.api_key,
            "Secret-Key": steadfast.secret_key
        }
        return requests.post(url, headers=headers, json=order_data)
    return None

class SteadFastOrderCreateAPI:
    def __init__(self, account):
        self.account = account
    
    def get_steadfast_credentials(self):
        try:
            steadfast = SteadFastAPI.objects.get(account=self.account)
            return steadfast
        except SteadFastAPI.DoesNotExist:
            return None

    def create_order(self, order_data):
        url = f"{self.get_steadfast_credentials().base_url}/create_order"
        headers = {
            "Content-Type": "application/json",
            "Api-Key": self.get_steadfast_credentials().api_key,
            "Secret-Key": self.get_steadfast_credentials().secret_key
        }
        response = requests.post(url, headers=headers, json=order_data)
        response.raise_for_status()
        return response.json()


def generate_unique_slug(model_object, field_value, old_slug=None):
    slug = slugify(field_value)
    if slug != old_slug:
        unique_slug = slug
        num = 1
        while model_object.objects.filter(slug=unique_slug).exists():
            if unique_slug == old_slug:
                return old_slug
            unique_slug = f'{slug}-{num}'
            num+=1
        return unique_slug
    else:
        return old_slug
