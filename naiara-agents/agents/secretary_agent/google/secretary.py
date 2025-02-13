from agno.models.message import Message
from typing import Optional, List, Union, Dict

from agno.agent import Agent
from agno.models.openai import OpenAIChat

from agents.settings import secretary_settings
from utils.constants import SECRETARY_AGENT


def get_secretary_agent(
    model_id: Optional[str] = None,
    user_id: Optional[str] = None,
    session_id: Optional[str] = None,
    debug_mode: bool = False,
    user_data: Optional[dict] = None,
    session_data: Optional[dict] = None,
    helper_message: Optional[List[Union[Dict, Message]]] = None) -> Agent:
    return Agent(
        name="Secretary Agent",
        agent_id=SECRETARY_AGENT,
        session_id=session_id,
        user_id=user_id,
        # session_state=session_data,  // todo look for old session's data
        # session_data=session_data,
        model=OpenAIChat(id=model_id or secretary_settings.gpt_4,
                         temperature=secretary_settings.default_temperature,
                         api_key=secretary_settings.secretary_api_key, ),
        tools=[],
        introduction=secretary_settings.introduction,
        # guidelines=secretary_settings.guidelines, // todo look for this
        description=secretary_settings.description,
        instructions=secretary_settings.instructions,
        # Format responses as markdown
        markdown=True,
        # Show tool calls in the response
        show_tool_calls=True,
        # Add the current date and time to the instructions
        add_datetime_to_instructions=True,
        # Store agent sessions in the database
        # storage=secretary_agent_storage, // todo fix storage
        # Enable read the chat history from the database
        read_chat_history=True,
        # Enable searching the knowledge base
        search_knowledge=True,
        # Enable monitoring on phidata.app
        monitoring=True,
        # Show debug logs
        debug_mode=debug_mode,
        add_history_to_messages=True,
        num_history_responses=20,
        # prevent_hallucinations=True,
        add_messages=helper_message,
        # add_context=False,
        # knowledge=travel_agent_knowledge,
        # limit_tool_access=True,
        # user_data=user_data,  # todo add user's data
        # structured_outputs=True,
        reasoning=False,
    )
