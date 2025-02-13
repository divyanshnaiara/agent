from agno.agent import Agent
from agno.knowledge import AgentKnowledge
from agno.models.message import Message
from typing import Optional, List, Union, Dict, Callable, Any
from agno.models.openai import OpenAIChat
from openai import BaseModel
from openai._compat import ConfigDict
from pydantic import Field

# from pydantic import BaseModel, Field, ConfigDict

from agents.settings import travel_settings
from agents.travel.tool import read_flights, ReadFlightsRequest
from utils.constants import TRAVEL_AGENT

# from pydantic import BaseModel, Field
from typing import List


class FlightDetail(BaseModel):
    flight_number: str = Field(..., description="Flight number.")
    departure_time: str = Field(..., description="Departure time of the flight.")
    arrival_time: str = Field(..., description="Arrival time of the flight.")
    duration: str = Field(..., description="Duration of the flight.")
    price: float = Field(..., description="Price of the flight.")
    currency: str = Field(..., description="Currency of the flight price.")
    airline: str = Field(..., description="Airline operating the flight.")

    model_config = ConfigDict(extra="forbid")  # Ensures no extra properties


class HotelDetail(BaseModel):
    hotel_name: str = Field(..., description="Name of the hotel.")
    location: str = Field(..., description="Location of the hotel.")
    price_per_night: float = Field(..., description="Price per night at the hotel.")
    rating: float = Field(..., description="Rating of the hotel.")

    model_config = ConfigDict(extra="forbid")  # Ensures no extra properties


class TravelAgentResponse(BaseModel):
    request: ReadFlightsRequest = Field(..., description="Original flight search request parameters.", strict=True)
    content: str = Field(..., description="Stores assistant's response chunks.")
    flights: List[FlightDetail] = Field(..., description="Array of flight details as received from the tool.")
    hotels: List[HotelDetail] = Field(..., description="Array of hotel details as received from the tool.")
    error: Optional[str] = Field(None, description="Stores any error message if something goes wrong.")

    model_config = ConfigDict(extra="forbid")  # Ensures no extra properties


def get_travel_agent(
        model_id: Optional[str] = None,
        knowledge_base: Optional[AgentKnowledge] = None,
        user_id: Optional[str] = None,
        session_id: Optional[str] = None,
        debug_mode: bool = False,
        user_data: Optional[dict] = None,
        session_data: Optional[dict] = None,
        system_message: Optional[Union[str, Callable, Message]] = None,
        helper_message: Optional[List[Union[Dict, Message]]] = None
) -> Agent:
    return Agent(
        name="Travel Agent",
        # model=Groq(id="llama3-8b-8192"),
        # model=Groq(id="llama-3.3-70b-versatile"),
        agent_id=TRAVEL_AGENT,
        session_id=session_id,
        user_id=user_id,
        model=OpenAIChat(id=travel_settings.gpt_4, api_key=travel_settings.api_key),
        tools=[read_flights],
        # tools=[{
        #     "name": "read_flights",
        #     "description": "Retrieves a list of available flights based on search criteria.",
        #     "parameters": {
        #         "type": "object",
        #         "properties": {
        #             "request": {
        #                 "type": "object",
        #                 "description": "Flight search parameters.",
        #                 "properties": {
        #                     "user_id": {"type": "string", "description": "Unique user_id from the run message."},
        #                     "From_IATACODE": {"type": "string", "description": "IATA code of the departure airport."},
        #                     "To_IATACODE": {"type": "string", "description": "IATA code of the arrival airport."},
        #                     "departure_date": {"type": "string", "description": "Departure date in YYYY-MM-DD format."},
        #                     "journey_type": {
        #                         "type": "string",
        #                         "enum": ["OneWay", "Return", "Circle"],
        #                         "description": "Type of journey (OneWay, Return, Circle)."
        #                     },
        #                     "flight_class": {
        #                         "type": "string",
        #                         "enum": ["First", "Business", "Economy", "PremiumEconomy"],
        #                         "description": "Flight class."
        #                     },
        #                     "adults": {"type": "integer", "description": "Number of adults."},
        #                     "children": {"type": "integer", "description": "Number of children."},
        #                     "infants": {"type": "integer", "description": "Number of infants."},
        #                     "return_date": {"type": ["string", "null"],
        #                                     "description": "Return date if applicable (YYYY-MM-DD)."},
        #                     "airline_code": {"type": ["string", "null"], "description": "Two-letter airline code."},
        #                     "direct_flight": {"type": ["integer", "null"],
        #                                       "description": "1 for direct flights only, 0 for both."},
        #                     "required_currency": {"type": "string", "default": "INR",
        #                                           "description": "Currency for the search."}
        #                 },
        #                 "required": [
        #                     "user_id", "From_IATACODE", "To_IATACODE", "departure_date",
        #                     "journey_type", "flight_class", "adults", "children", "infants"
        #                 ],
        #                 "additionalProperties": False  # ✅ This fixes the OpenAI schema error
        #             }
        #         },
        #         "required": ["request"],
        #         "additionalProperties": False  # ✅ Ensures only defined properties are accepted
        #     }
        # }
        # ],
        introduction='''Travel Agent Assistant is an intelligent travel-planning assistant designed to help users effortlessly find and manage flights, accommodations, and itineraries. With access to real-time flight information and personalized search capabilities, the Travel Agent Assistant can filter and suggest flights based on preferences like dates, times, budget, and preferred airlines. It also offers hotel recommendations, travel insurance options, and destination insights, ensuring a seamless travel experience from start to finish.
By integrating with major travel and flight APIs, Travel Agent Assistant ensures accurate, up-to-date travel options and provides users with itinerary summaries, booking reminders, and timely notifications for smooth and organized travel.''',
        #         guidelines=['''Travel Agent Assistant is an intelligent travel-planning assistant designed to help users effortlessly find and manage flights, accommodations, and itineraries. With access to real-time flight information and personalized search capabilities, the Travel Agent Assistant can filter and suggest flights based on preferences like dates, times, budget, and preferred airlines. It also offers hotel recommendations, travel insurance options, and destination insights, ensuring a seamless travel experience from start to finish.
        #
        # By integrating with major travel and flight APIs, Travel Agent Assistant ensures accurate, up-to-date travel options and provides users with itinerary summaries, booking reminders, and timely notifications for smooth and organized travel.''', r'''For each flight, ensure the response strictly adheres to the following format, capturing all specified details using the provided Regex structure. Each detail should appear exactly as described below, (give 0 stop for non-stop):
        # r'\*\*Airline\*\*: (?<airline>.+?)\s*' // Captures Airline
        #       r'- \*\*Flight Number\*\*: (?<flightNumber>.+?)\s*' // Captures Flight Number
        #       r'- \*\*Departure\*\*: (?<departureAirportCode>.+?) at (?<departureTime>\d{2}:\d{2})\s*' // Captures Departure Airport Code and Time
        #       r'- \*\*Arrival\*\*: (?<arrivalAirportCode>.+?) at (?<arrivalTime>\d{2}:\d{2})\s*' // Captures Arrival Airport Code and Time
        #       r'- \*\*Duration\*\*: (?<duration>.+?)\s*' // Captures Duration
        #       r'- \*\*Price\*\*: (?<currencySymbol>[^\d\s]+)(?<price>[\d,]+)\s*' // Captures Price with any currency symbol
        #       r'- \*\*Travel Class\*\*: (?<travelClass>.+?)\s*' // Captures Travel Class
        #       r'- \*\*Legroom\*\*: (?<legroom>.+?)\s*' // Captures Legroom
        #       r'- \*\*Carbon Emissions\*\*: (?<carbonEmissions>\d+ kg) \((?<carbonDetails>.+?)\)\s*' // Captures Carbon Emissions
        #       r'- \*\*Flight Link\*\*: \[(?<linkText>[^\]]+)\]\((?<link>[^\)]+)\)\s*'
        #      r'- \*\*Image\*\*: \!\[(?<imageAltText>[^\]]+)\]\((?<imageUrl>[^\)]+)\)\s*'
        #       r'- \*\*Stops\*\*: (?<numberOfStops>0 stops?|1 stop|\d+ stops?)\s*(?:\((?<stopAirports>[A-Z]{3}(?:, [A-Z]{3})*)\))?\s*'// Captures Stops
        #       r'- \*\*Trip Type\*\*: (?<tripType>.+?)'''],
        #         introduction=travel_settings.introduction,
        # guidelines=secretary_settings.guidelines, // todo look for this
        description=travel_settings.description,
        instructions=travel_settings.instructions,
        # instructions=travel_settings.instructions,
        #         instructions=["Initially Greet User with the user's name", '''The Travel Agent Assistant offers three main functions:
        #
        # Flight Management:
        # Fetch Flights: Find flights based on user-provided details such as origin, destination, travel dates, preferred airlines, and budget. Show a list of suitable options, including details like departure and arrival times, layovers, and ticket prices.
        #
        # Filter Results: Refine search results based on user preferences, such as shortest duration, lowest price, or specific time ranges for departure and arrival.
        #
        # Update & Notify: If any flight details change after booking, notify the user immediately and provide options for rebooking or adjusting the itinerary.
        #
        # Suggest Alternatives: If specific criteria can't be met (e.g., no flights at a particular time), suggest alternative dates, airlines, or travel routes.
        #
        # Accommodation and Travel Planning:
        # Search Accommodations: Based on travel dates and destination, search for available hotels, rental properties, and other lodging options that match user preferences for location, price, and amenities.
        #
        # Itinerary Creation: Organize booked flights and accommodations into a coherent itinerary, adding relevant details like check-in/check-out times and local time zones.
        #
        # Update Travel Plans: Modify or adjust the itinerary based on any changes in flights, accommodations, or user requests.
        #
        # Travel Notifications and Assistance:
        # Send Alerts: Notify the user of any relevant updates, such as price drops, delays, or cancellations for previously viewed or booked travel plans.
        #
        # Provide Travel Insights: Offer helpful destination-specific tips, such as local weather, transportation options, visa requirements, and health and safety advisories.
        #
        # Throughout each interaction, Travel Agent Assistant maintains a friendly, supportive tone, confirming details before proceeding with any bookings or updates to ensure an organized and stress-free travel experience.'''],
        add_history_to_messages=True,
        num_history_responses=5,
        # add_context=False,
        knowledge=knowledge_base,
        show_tool_calls=False,
        # Add the current date and time to the instructions
        add_datetime_to_instructions=True,
        # Store agent sessions in the database
        # storage=secretary_agent_storage, // todo fix storage
        # Enable read the chat history from the database
        read_chat_history=True,
        read_tool_call_history=True,
        # Enable searching the knowledge base
        search_knowledge=True,
        # Enable monitoring on agno.com
        monitoring=True,
        # Show debug logs
        debug_mode=debug_mode,
        # prevent_hallucinations=True,
        add_messages=helper_message,
        # user_id=uid,
        # user_data=user_data,
        reasoning=False,

        # prevent_hallucinations=True,
        # stream_intermediate_steps=True,
        # reasoning_steps=None,
        # add_messages=[msg_dict],
        # limit_tool_access=True,
        # user_data=user_data,  # todo add user's data
        # structured_outputs=True,
        response_model=TravelAgentResponse,
        parse_response=True,
        structured_outputs=True,
        markdown=True,
        stream=True
    )
