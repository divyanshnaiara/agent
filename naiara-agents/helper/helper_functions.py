from typing import Optional, Union, Callable

from agno.knowledge import AgentKnowledge
from agno.models.message import Message

from agents.secretary_agent.google.secretary import get_secretary_agent
from agents.shopper_agent.shopper_agent import get_shopper_agent
from agents.travel.travel_agent import get_travel_agent
from utils.constants import SECRETARY_AGENT, TRAVEL_AGENT, SHOPPER_AGENT


def get_agent(user_id: Optional[str] = None,
              session_id: Optional[str] = None,
              debug_mode: bool = False,
              agent_id: Optional[str] = None,
              context: Optional[Union[str, Callable, Message]] = None,
              knowledge_base: Optional[AgentKnowledge] = None,
              ):
    """Checks for the agent in requested """
    if agent_id == SECRETARY_AGENT:
        return get_secretary_agent(user_id=user_id, session_id=session_id, debug_mode=debug_mode)
    elif agent_id == TRAVEL_AGENT:
        return get_travel_agent(user_id=user_id, session_id=session_id, debug_mode=True, system_message=context,
                                helper_message=[{"userId": user_id, "sessionId": session_id}],
                                knowledge_base=knowledge_base, )
    elif agent_id == SHOPPER_AGENT:
            return get_shopper_agent(user_id=user_id, session_id=session_id, debug_mode=debug_mode)
    return
