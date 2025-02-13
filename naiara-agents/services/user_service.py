import json
import os

from typing import Optional, Iterator, Callable, Union, Dict, Any

from dotenv import load_dotenv

from models.user import User
from utils.constants import METHOD_GET, METHOD_POST
from web.request import make_request

load_dotenv()
USER_SERVICE_URL = os.getenv('USER_SERVICE_URL')


async def get_user_by_uid(uid) -> User or None:
    url = USER_SERVICE_URL + "retrieveUser"
    print("User svc URL: {}".format(url))
    try:
        response = make_request(url=url, method=METHOD_GET, params={"uid": uid})
        if response.status_code == 200:
            print("user response :: ", response.json())
            return User.from_dict(response.json())
        elif response.status_code == 500:
            print("Internal Server Error (500) from user service")
            return None  # Or return {"error": "Internal Server Error"}

        else:
            print(f"Unexpected error: {response.status_code}, Response: {response.text}")
            return None
    # Or return {"error": "User service unreachable"}
    except Exception as e:
        print(f"Unhandled exception: {e}")
    return None


async def update_user(user: User) -> Optional[Dict[str, Any]] or None:
    url = USER_SERVICE_URL + "updateUser"
    print("User svc URL: {}".format(url))
    try:
        # Convert the user object to a dictionary before sending the request
        user_data = user.to_dict() if hasattr(user, "to_dict") else user.__dict__
        # Ensure 'providers' field is a list of dictionaries
        if "providers" in user_data and isinstance(user_data["providers"], list):
            user_data["providers"] = [
                provider.to_dict() if hasattr(provider, "to_dict") else provider.__dict__
                for provider in user_data["providers"]
            ]

        print("User data ::", json.dumps(user_data, indent=2))  # Pretty print JSON for debugging

        # print("User data :: ", user_data)

        response = make_request(url=url, method=METHOD_POST, data=user_data,
                                headers={"Content-Type": "application/json"})

        if response.status_code == 200:
            print("User update successful ::", response.json())
            return response.json()
        elif response.status_code == 500:
            print("Internal Server Error (500) from user service")
            return None  # Or return {"error": "Internal Server Error"}
        else:
            print(f"Unexpected error: {response.status_code}, Response: {response.text}")
            return None
    except Exception as e:
        print(f"Unhandled exception: {e}")
        return None
