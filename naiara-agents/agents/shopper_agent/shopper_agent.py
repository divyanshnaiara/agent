from readline import add_history

from agno.agent import Agent
from agno.knowledge import AgentKnowledge
from agno.models.message import Message
from typing import Optional, List, Dict,Union,Callable
from agno.models.openai import OpenAIChat

from agents.shopper_agent.tool import search_products
from utils.constants import SHOPPER_AGENT
from agents.settings import shopper_setting


def get_shopper_agent(
        user_id: Optional[str]=None,
        session_id: Optional[str]=None,
        debug_mode: bool=False,
        helper_message: Optional[List[Union[Dict, Message]]] = None
)->Agent:
    return Agent(
        name="Shopper Agent",
        agent_id=SHOPPER_AGENT,
        session_id=session_id,
        user_id=user_id,
        tools=[search_products],
        introduction= '''Shopper Agent is an intelligent shopping assistant designed to help users find and manage their shopping needs effortlessly. From product discovery to purchase tracking, it streamlines the shopping experience by providing real-time product availability and personalized search options based on price, brand, category, and user reviews.By integrating with major e-commerce platforms and retailer APIs, Shopper Agent ensures accurate and up-to-date product listings. It offers users a clear overview of product details, including amount, rating, description, name, image, and URL, making shopping more convenient and efficient.
Whether you're looking for the best products or keeping track of your purchases, Shopper Agent provides a smooth and organized shopping experience.''',
    add_history_to_messages=True,
        description= shopper_setting.description,
        instructions=shopper_setting.instructions,
    num_history_responses=5,
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
    markdown=True,
    stream=True
    )