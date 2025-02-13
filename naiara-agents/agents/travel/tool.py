import json
from typing import Optional

import httpx
from enum import Enum

from dotenv import load_dotenv
from pydantic import BaseModel, Field, ConfigDict

from utils.constants import INTEGRATION_SERVICE_URL, METHOD_POST
from web.request import make_request


# Define Enums for fixed values
class JourneyType(str, Enum):
    ONEWAY = "OneWay"
    RETURN = "Return"
    CIRCLE = "Circle"


class FlightClass(str, Enum):
    FIRST = "First"
    BUSINESS = "Business"
    ECONOMY = "Economy"
    PREMIUM_ECONOMY = "PremiumEconomy"


class ReadFlightsRequest(BaseModel):
    # user_id: str = Field(..., description="Unique user_id from the run message.")
    From_IATACODE: str = Field(..., description="IATA code of the departure airport.")
    To_IATACODE: str = Field(..., description="IATA code of the arrival airport.")
    departure_date: str = Field(..., description="Departure date in YYYY-MM-DD format.")
    journey_type: JourneyType = Field(JourneyType.ONEWAY, description="Type of journey (OneWay, Return, Circle).")
    flight_class: FlightClass = Field(FlightClass.ECONOMY,
                                      description="Flight class (First, Business, Economy, PremiumEconomy).")
    adults: str = Field(..., description="Number of adults.")
    children: str = Field(..., description="Number of children.")
    infants: str = Field(..., description="Number of infants.")
    return_date: Optional[str] = Field(None,
                                       description="Return date if applicable (YYYY-MM-DD, required for Return journeyType).")
    airline_code: Optional[str] = Field(None, description="Two-letter airline code.")
    direct_flight: Optional[str] = Field(None,
                                         description="1 for direct flights only, 0 for both direct and layover flights.")
    required_currency: str = Field("INR", description="Currency for the search (default: INR).")

    class Config:
        extra = "forbid"  # Ensures no extra properties


def read_flights(
        #         user_id: str,
        #         From_IATACODE: str,
        #         To_IATACODE: str,
        #         departure_date: str,
        #         journey_type: JourneyType = JourneyType.ONEWAY,
        #         flight_class: FlightClass = FlightClass.ECONOMY,
        #         adults: str = "1",
        #         children: str = "0",
        #         infants: str = "0",
        #         return_date: str = None,
        #         airline_codes: list[str] = None,
        #         required_currency: str = "INR"
        request: ReadFlightsRequest

) -> str:
    """
    Retrieves a list of available flights based on search criteria and returns minimum 10 results.
    If journey_type / flight_class gets missing use OneWay / Economy as a default flight class.

     Args:
        request (ReadFlightsRequest): Pydantic model containing flight search parameters.

    additionalProperties: false

    Returns:
        str: JSON string of available flights.
    """
    url = f"{INTEGRATION_SERVICE_URL}fetchFlights"  # Replace with actual API endpoint
    print("INTEGRATION_SERVICE_URL : ", url)

    payload = {

        "uid": "user_id",  # todo remove
        "body": {
            "AdultCount": str(request.adults),
            "ChildCount": str(request.children),
            "InfantCount": str(request.infants),
            "JourneyType": request.journey_type.value,
            "CabinClass": request.flight_class.value,
            "Segments": [
                {
                    "Origin": request.From_IATACODE,
                    "Destination": request.To_IATACODE,
                    "DepartureDate": request.departure_date
                }
            ]
        }
    }

    if request.journey_type == JourneyType.RETURN and request.return_date:
        payload["body"]["Segments"].append({
            "Origin": request.To_IATACODE,
            "Destination": request.From_IATACODE,
            "DepartureDate": request.return_date
        })

    print("Json Payload : ", payload)
    try:
        response = make_request(METHOD_POST, url, params=None, data=payload,
                                headers={"Content-Type": "application/json"})
        print("Response of Integration service : ", response.json())
        return json.dumps(response.json())
    except httpx.HTTPError as e:
        return json.dumps({"error": str(e)})
