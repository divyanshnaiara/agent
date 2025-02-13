import json
import httpx

from dotenv import load_dotenv
from models.user import User
from utils.constants import INTEGRATION_SERVICE_URL

def search_products(
        user_id: str,
        query: str,
        country: str,
        sort_by: str = "RELEVANCE",
        page: int = 1,
        is_prime: bool = False
) -> str:
    """
    Retrieves a list of available products or stores based on search criteria.

    Args:
        user_id (str): Unique user_id from the run message.
        query (str): Search query for products or stores.
        country (str): Country code for localized results.
        sort_by (str, optional): Sorting criteria (default: "RELEVANCE").
        page (int, optional): Page number for paginated results (default: 1).
        is_prime (bool, optional): Filter for Prime-eligible products (default: False).

    Returns:
        str: JSON string of available products or stores.
    """
    url = f"{INTEGRATION_SERVICE_URL}fetchProducts"  # Replace with actual API endpoint
    print("User in function: ", User)
    print("INTEGRATION_SERVICE_URL: ", INTEGRATION_SERVICE_URL)

    payload = {
        "uid": user_id,
        "query": query,
        "country": country,
        "sort_by": sort_by,
        "page": page,
    }
    print("payload: ", payload)

    if is_prime:
        payload["is_prime"] = is_prime

    try:
        response = httpx.post(url, json=payload, timeout=120)
        response.raise_for_status()
        # return response.json()
        print("Status code: ", response.status_code)
        print("Response from Integration service: ", response.json())
        return json.dumps(response.json())
    except httpx.HTTPError as e:
        return json.dumps({"error": str(e)})
