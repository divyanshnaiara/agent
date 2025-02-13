import requests
from typing import Optional, Dict, Any


def make_request(method: str, url: str, params: Optional[Dict[str, Any]] = None, data: Optional[Dict[str, Any]] = None,
                 headers: Optional[Dict[str, str]] = None) -> Optional[requests.Response]:
    """
    A common function to make GET and POST requests.

    :param method: HTTP method ('GET' or 'POST')
    :param url: API endpoint
    :param params: Query parameters for GET request
    :param data: Payload for POST request
    :param headers: Request headers
    :return: Response object or None in case of failure
    """
    try:
        if method.upper() == "GET":
            response = requests.get(url, params=params, headers=headers)
        elif method.upper() == "POST":
            response = requests.post(url, json=data, headers=headers)
        else:
            raise ValueError("Invalid HTTP method. Use 'GET' or 'POST'.")

        # response.raise_for_status()  # Raise an error for bad status codes
        return response
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None