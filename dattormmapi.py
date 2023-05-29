"""
Functions to interact with DattoRMM API    
"""

import requests


def dattormm_get_token(api_url: str, api_key: str, api_secret_key: str) -> str:
    """
    Get comms token for DattoRMM API

    Args:
        api_url (str): URL for DattoRMM API end point
        api_key (str): DattoRMM API Key
        api_secret_key (str): DattoRMM API Secret Key

    Returns:
        str: DattoAPI Access Token for this communication
    """
    headers = {"ContentType": "application/x-www-form-urlencoded"}
    api_uri = f"{api_url}/auth/oauth/token"
    token_request_payload = {"grant_type": "password", "username": api_key, "password": api_secret_key}

    response = requests.post(url=api_uri, data=token_request_payload, headers=headers, auth=("public-client", "public"), timeout=5)

    if response.status_code != 200:
        print("Failed to get token")
        return ""

    tokens = response.json()
    return tokens["access_token"]


def dattormm_api_request(api_uri: str, api_access_token: str, api_request_body: str):
    """
    Request data from DattoRMM API

    Args:
        api_url (str): API Url
        api_access_token (str): Access token
        api_request (str): API Request
        api_request_body (str): Body of API request

    Returns:
        _type_: JSON formatted response
    """

    headers = {"Authorization": f"Bearer {api_access_token}", "ContentType": "application/json"}

    # 	# Make request
    response = requests.get(api_uri, headers=headers, data=api_request_body, timeout=5)

    if response.status_code != 200:
        print("Failed Request")
        return ""

    return response.json()
