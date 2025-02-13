from agents.secretary_agent.google.secretary import get_secretary_agent
from typing import Iterator, Optional

from agno.run.response import RunResponse
from starlette.websockets import WebSocket
from starlette.websockets import WebSocketDisconnect


# @app.websocket("/secretary")
# async def secretary_agent(websocket: WebSocket,
#                        user_id: Optional[str] = None,
#                        session_id: Optional[str] = None,
#                        debug_mode: bool = False
#                        ):
#     await websocket.accept()
#     # Extract query parameters
#     user_id = websocket.query_params.get("userId", user_id)
#     session_id = websocket.query_params.get("sessionId", session_id)
#     agent = get_secretary_agent(user_id=user_id, session_id=session_id, debug_mode=debug_mode)
#
#     try:
#         while True:
#             data = await websocket.receive_text()
#             response_stream: Iterator[RunResponse] = agent.run(data, stream=True)
#             # p = Playground(agents=[agent])
#             print(f"User: {user_id}, Session: {session_id}, Debug: {debug_mode}")
#             print("Response stream:", response_stream)
#             for response in response_stream:
#                 await websocket.send_json(response.to_dict())
#                 print("response metrics :: ", response.metrics)
#             # await websocket.send_text(f"RESP: {response_stream}")
#     except WebSocketDisconnect:
#         print("WebSocket connection closed for user {user_id}, session {session_id}")
