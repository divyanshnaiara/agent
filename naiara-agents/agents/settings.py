import os
from typing import Optional, List, Callable, Union

from pydantic_settings import BaseSettings

from utils.strings import TRAVEL_AGENT_DESCRIPTION, SHOPPER_AGENT_DESCRIPTION


class AgentSettings(BaseSettings):
    """Agent settings that can be set using environment variables.

    Reference: https://pydantic-docs.helpmanual.io/usage/settings/
    """

    gpt_4: str = "gpt-4o"
    embedding_model: str = "text-embedding-3-small"
    api_key: Optional[str] = os.getenv("OPENAI_API_KEY")
    # default_max_completion_tokens: int = 16000
    default_temperature: float = 0.2
    instructions: Optional[Union[str, List[str], Callable]] = None
    introduction: Optional[str] = None
    description: Optional[str] = None
    # guidelines: Optional[List[str]] = None


# Create an AgentSettings object

'''Set introduction , description, guidelines related strings here'''
secretary_settings = AgentSettings(introduction="hey you are secretary agent",
                                   description="You are good secretary agent to schedule events")
travel_settings = AgentSettings(introduction='you ar good travel agent', description=TRAVEL_AGENT_DESCRIPTION,
                                instructions=[
                                    "If user misses any of the details like class or journey_type then user OneWay for journey_type and Economy for flight_class",
                                    "Be specific with the source and destination mentioned by user as if a slight change in these can occur a huge loss in my business",
                                    "fetch IATA code from knowledge database if not found in knowledge database or some error occurs then use standard code ",
                                    "Ensure that the response contains at least 10 flight results. ",
                                    "If fewer than 10 results are available, adjust the search parameters dynamically ",
                                    "(such as broader date ranges, nearby airports, or alternative airlines) to retrieve more options. ",
                                    "Do not duplicate results; instead, expand the search scope to meet the minimum count.",
                                    "Strictly Follow the below regex while generating response for tool call",
                                    r'''
                                    For each flight, ensure the response strictly adheres to the following format, capturing all specified details using the provided Regex structure. Each detail should appear exactly as described below, (give 0 stop for non-stop):
                                          r'\*\*Airline\*\*: (?<airline>.+?)\s*' // Captures Airline
                                          r'- \*\*Flight Number\*\*: (?<flightNumber>.+?)\s*' // Captures Flight Number
                                          r'- \*\*Departure\*\*: (?<departureAirportCode>.+?) at (?<departureTime>\d{2}:\d{2})\s*' // Captures Departure Airport Code and Time
                                          r'- \*\*Arrival\*\*: (?<arrivalAirportCode>.+?) at (?<arrivalTime>\d{2}:\d{2})\s*' // Captures Arrival Airport Code and Time
                                          r'- \*\*Duration\*\*: (?<duration>.+?)\s*' // Captures Duration
                                          r'- \*\*Price\*\*: (?<currencySymbol>[^\d\s]+)(?<price>[\d,]+)\s*' // Captures Price with any currency symbol
                                          r'- \*\*Travel Class\*\*: (?<travelClass>.+?)\s*' // Captures Travel Class
                                          r'- \*\*Legroom\*\*: (?<legroom>.+?)\s*' // Captures Legroom
                                          r'- \*\*Carbon Emissions\*\*: (?<carbonEmissions>\d+ kg) \((?<carbonDetails>.+?)\)\s*' // Captures Carbon Emissions
                                          r'- \*\*Flight Link\*\*: \[(?<linkText>[^\]]+)\]\((?<link>[^\)]+)\)\s*'
                                          r'- \*\*Image\*\*: \!\[(?<imageAltText>[^\]]+)\]\((?<imageUrl>[^\)]+)\)\s*'
                                          r'- \*\*Stops\*\*: (?<numberOfStops>0 stops?|1 stop|\d+ stops?)\s*(?:\((?<stopAirports>[A-Z]{3}(?:, [A-Z]{3})*)\))?\s*'// Captures Stops
                                          r'- \*\*Trip Type\*\*: (?<tripType>.+?)'




                                    Always send the response for the hotel tool calls that satisfies the below Regex  strictly for every single hotel details
                                      r'\*\*(?<name>[^\*]+)\*\*' //Captures the hotel name
                                      r'- \*\*Rating\*\*: (?<rating>\d+\.\d)\s*' // Captures Rating
                                      r'- \*\*Price\*\*: (?<currencySymbol>[^\d\s]+)(?<price>[\d,]+) (?: per night)?\s*' // Captures Price with any currency symbol
                                      r'- \*\*Description\*\*: (?<description>.+?)\s*' // Captures Description
                                      r'- \*\*Link\*\*: \[(?<linkText>[^\]]+)\]\((?<link>[^\)]+)\)\s*' // Captures Link Text and URL
                                      r'- \*\*Image\*\*: \!\[(?<imageAltText>[^\]]+)\]\((?<imageUrl>[^\)]+)\)', // Captures Image Alt Text and URL
                                      multiLine: true,



                                    ensure that markdown satisfies the below function

                                     _validateData(String data) {
                                        String cleanedData = data
                                            .replaceAll(RegExp(r'^.*:\s*'), '')
                                            .replaceAll(RegExp(r'I/flutter \(\d+\):\s*'), '')
                                            .trim();
                                        _extractDetails(cleanedData);
                                      }

                                     _extractDetails(String markDownDetails) {
                                        // To store NEW flights or hotels data in list

                                        List<Map<String, dynamic>> _flights = [];
                                        List<Map<String, dynamic>> _hotels = [];
                                    final RegExp flightRegex = RegExp(
                                    r'\*\*Airline\*\*: (?<airline>.+?)\s*' // Captures Airline
                                          r'- \*\*Flight Number\*\*: (?<flightNumber>.+?)\s*' // Captures Flight Number
                                          r'- \*\*Departure\*\*: (?<departureAirportCode>.+?) at (?<departureTime>\d{2}:\d{2})\s*' // Captures Departure Airport Code and Time
                                          r'- \*\*Arrival\*\*: (?<arrivalAirportCode>.+?) at (?<arrivalTime>\d{2}:\d{2})\s*' // Captures Arrival Airport Code and Time
                                          r'- \*\*Duration\*\*: (?<duration>.+?)\s*' // Captures Duration
                                          r'- \*\*Price\*\*: (?<currencySymbol>[^\d\s]+)(?<price>[\d,]+)\s*' // Captures Price with any currency symbol
                                          r'- \*\*Travel Class\*\*: (?<travelClass>.+?)\s*' // Captures Travel Class
                                          r'- \*\*Legroom\*\*: (?<legroom>.+?)\s*' // Captures Legroom
                                          r'- \*\*Carbon Emissions\*\*: (?<carbonEmissions>\d+ kg) \((?<carbonDetails>.+?)\)\s*' // Captures Carbon Emissions
                                          r'- \*\*Flight Link\*\*: \[(?<linkText>[^\]]+)\]\((?<link>[^\)]+)\)\s*'
                                          r'- \*\*Image\*\*: \!\[(?<imageAltText>[^\]]+)\]\((?<imageUrl>[^\)]+)\)\s*'
                                          r'- \*\*Stops\*\*: (?<numberOfStops>0 stops?|1 stop|\d+ stops?)\s*(?:\((?<stopAirports>[A-Z]{3}(?:, [A-Z]{3})*)\))?\s*'// Captures Stops
                                          r'- \*\*Trip Type\*\*: (?<tripType>.+?)',
                                      multiLine: true,
                                    caseSensitive:false
                                    dotAll: true,
                                    );


                                        final RegExp hotelRegex = RegExp(
                                          r'^(?<name>.+?)\s*' // Captures the hotel name
                                          r'- \*\*Rating\*\*: (?<rating>\d+\.\d)\s*' // Captures Rating
                                          r'- \*\*Price\*\*: (?<currencySymbol>[^\d\s]+)(?<price>[\d,]+)(?: per night)?\s*' // Captures Price with any currency symbol
                                          r'- \*\*Description\*\*: (?<description>.+?)\s*' // Captures Description
                                          r'- \*\*Link\*\*: \[(?<linkText>[^\]]+)\]\((?<link>[^\)]+)\)\s*' // Captures Link Text and URL
                                          r'- \*\*Image\*\*: \!\[(?<imageAltText>[^\]]+)\]\((?<imageUrl>[^\)]+)\)',
                                          multiLine: true,
                                          dotAll: true,
                                        );

                                        var hotelMatches = hotelRegex.allMatches(markDownDetails);

                                        var flightMatches = flightRegex.allMatches(markDownDetails);'''
                                ])

shopper_setting = AgentSettings(introduction= "Hey you are shopper agent", description= SHOPPER_AGENT_DESCRIPTION,
                                instructions=[
                                    "If the user misses any details like product category or brand, default to a general category and popular brand.",
                                    "Ensure product names and specifications are accurate, as slight change in these can occur a huge loss in my business",
                                    "Ensure the response contains at least 10 product results.",
                                    "Do not duplicate results; instead, expand the search scope to meet the minimum count.",
                                    "Strictly follow the below regex while generating responses for tool calls:",
                                    r''' 
                                        For each product, ensure the response strictly adheres to the following format, capturing all specified details using the provided Regex structure. Each detail should appear exactly as described below: 
                                            r'\*\*Product Name\*\*: (?<productName>.+?)\s*' // Captures Product Name  
                                            r'- \*\*Price\*\*: (?<currencySymbol>[^\d\s]+)(?<price>[\d,]+)\s*' // Captures Price with any currency symbol  
                                            r'- \*\*Rating\*\*: (?<rating>\d+\.\d)\s*' // Captures Rating  
                                            r'- \*\*Description\*\*: (?<description>.+?)\s*' // Captures Product Description  
                                            r'- \*\*Product Link\*\*: \[(?<linkText>[^\]]+)\]\((?<link>[^\)]+)\)\s*' // Captures Product Link  
                                            r'- \*\*Image\*\*: \!\[(?<imageAltText>[^\]]+)\]\((?<imageUrl>[^\)]+)\)\s*' // Captures Product Image  
                                             Always ensure the response satisfies the below function validation:  
                                                
                                                    _validateData(String data) {  
                                                        String cleanedData = data  
                                                            .replaceAll(RegExp(r'^.*:\s*'), '')  
                                                            .replaceAll(RegExp(r'I/flutter \(\d+\):\s*'), '')  
                                                            .trim();  
                                                        _extractDetails(cleanedData);  
                                                    } 
                                                 _extractDetails(String markDownDetails) {  
                                                      // To store NEW product data in a list  
                                            
                                                    List<Map<String, dynamic>> _products = [];  
                                                    final RegExp productRegex = RegExp(  
                                                        r'\*\*Product Name\*\*: (?<productName>.+?)\s*' // Captures Product Name  
                                                        r'- \*\*Price\*\*: (?<currencySymbol>[^\d\s]+)(?<price>[\d,]+)\s*' // Captures Price  
                                                        r'- \*\*Rating\*\*: (?<rating>\d+\.\d)\s*' // Captures Rating  
                                                        r'- \*\*Description\*\*: (?<description>.+?)\s*' // Captures Description  
                                                        r'- \*\*Product Link\*\*: \[(?<linkText>[^\]]+)\]\((?<link>[^\)]+)\)\s*' // Captures Link  
                                                        r'- \*\*Image\*\*: \!\[(?<imageAltText>[^\]]+)\]\((?<imageUrl>[^\)]+)\)\s*' // Captures Image   
                                                        multiLine: true,  
                                                        caseSensitive: false,  
                                                        dotAll: true,  
                                                    );  
                                            
                                                    var productMatches = productRegex.allMatches(markDownDetails);  
                                                }'''   ])
