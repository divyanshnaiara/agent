import os
import uuid
from typing import Optional, Iterator, Callable, Union, Dict

from agno.agent import Agent
from agno.models.message import Message
from agno.run.response import RunResponse
from fastapi import FastAPI
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from starlette.websockets import WebSocket, WebSocketDisconnect

from helper.helper_functions import get_agent
from models.user import User
from services.user_service import get_user_by_uid, update_user
from utils.constants import TRAVEL_AGENT, SECRETARY_AGENT
from agno.knowledge.json import JSONKnowledgeBase
from agno.vectordb.pgvector import PgVector

# Load environment variables from .env file
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
print("OPENAI_API_KEY::", OPENAI_API_KEY)

# def create_app() -> FastAPI:
#     """Create a FastAPI App
#
#     Returns:
#         FastAPI: FastAPI App
#     """
#
#     # Create FastAPI App
#     app: FastAPI = FastAPI(
#         title=api_settings.title,
#         version=api_settings.version,
#         docs_url="/docs" if api_settings.docs_enabled else None,
#         redoc_url="/redoc" if api_settings.docs_enabled else None,
#         openapi_url="/openapi.json" if api_settings.docs_enabled else None,
#     )
#
#     # Add v1 router
#     app.include_router(v1_router)
#
# Add Middlewares
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=api_settings.cors_origin_list,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
#
#     return app


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to a specific domain if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#
# if not PgVector.table_exists(PgVector(
#         table_name="airport_documents",
#         db_url=os.getenv("DB_URL"),
# )):
#     print("Table does not exist, creating:: ")
#     PgVector.create(PgVector(
#         table_name="airport_documents",
#         db_url=os.getenv("DB_URL"),
#     ))
#     print("DB created :: ", PgVector.table_exists(PgVector(
#         table_name="airport_documents",
#         db_url=os.getenv("DB_URL"),
#     )))
knowledge_base = JSONKnowledgeBase(
    path="./airports.json",
    vector_db=PgVector(
        table_name="airport_documents",
        db_url=os.getenv("DB_URL"),
    )
)
print("knowledge base:", knowledge_base)


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}  # Mapping session_id -> WebSocket

    async def connect(self, websocket: WebSocket, session_id: str):
        await websocket.accept()
        self.active_connections[session_id] = websocket  # Store connection by session_id

    def disconnect(self, session_id: str):
        if session_id in self.active_connections:
            del self.active_connections[session_id]

    async def send_personal_message(self, message: str, session_id: str):
        """Send message to a specific client"""
        websocket = self.active_connections.get(session_id)
        if websocket:
            await websocket.send_json({
                "type": "new_message",
                "payload": {
                    "userInput": {
                        "role": "",
                        "text": ""
                    },
                    "message": message,
                    "gptText": message,
                    "from": "gpt",
                    "sent": ""
                }
            })

    async def broadcast(self, message: dict):
        """Send message to all connected clients"""
        for websocket in self.active_connections.values():
            await websocket.send_json(message)


manager = ConnectionManager()


@app.get("/")
async def root():
    return {"message": "Welcome to Naiara Agents!"}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket,
                             user_id: Optional[str] = None,
                             session_id: Optional[str] = None,
                             debug_mode: bool = False,
                             agent_id: Optional[str] = None,
                             context: Optional[Union[str, Callable, Message]] = None,
                             ):
    # Extract query parameters
    user_id = websocket.query_params.get("userId", user_id)
    session_id = websocket.query_params.get("sessionId", session_id)
    agent_id = websocket.query_params.get("agentId", agent_id)
    context = websocket.query_params.get("context", context)

    # todo add user existence functionality
    user_details: User = await  get_user_by_uid(user_id)
    print("user_details:", user_details)
    if not user_details:
        print(f"WebSocket connection closed for user {user_id}, session {session_id}")
        await websocket.send_json({
            "type": "new_message",
            "payload": {
                "userInput": {
                    "role": "",
                    "text": ""
                },
                "message": "Something went wrong",
                "gptText": "Something went wrong",
                "from": "gpt",
                "sent": ""
            }
        })
        await websocket.close()
        return

    print(f"User Details : {user_details}")

    if not session_id:
        session_id = uuid.uuid4().hex
        if user_details.threadIds is None:
            user_details.threadIds = []
        user_details.threadIds.append(session_id)
        await update_user(user_details)

    print("Session ID:", session_id)

    # Connect the user WebSocket to the session
    await manager.connect(websocket, session_id)

    """Checks for the agent in requested """
    # if agent_id == SECRETARY_AGENT:
    #     agent = get_secretary_agent(user_id=user_id, session_id=session_id, debug_mode=debug_mode)
    # elif agent_id == TRAVEL_AGENT:
    #     agent = get_travel_agent(user_id=user_id, session_id=session_id, debug_mode=True, system_message=context,
    #                              helper_message=[{"userId": user_id, "sessionId": session_id}],
    #                              knowledge_base=knowledge_base, )
    # else:
    #     print(f"Invalid agent_id: {agent_id}")
    #     await websocket.send_json({
    #         "type": "new_message",
    #         "payload": {
    #             "userInput": {
    #                 "role": "",
    #                 "text": ""
    #             },
    #             "message": "Something went wrong",
    #             "gptText": "Something went wrong",
    #             "from": "gpt",
    #             "sent": ""
    #         }
    #     })
    #     await websocket.close()
    #     return

    try:
        agent = get_agent(agent_id=agent_id, user_id=user_id, session_id=session_id, debug_mode=True, context=context,
                          knowledge_base=knowledge_base)
        if not agent:
            await manager.send_personal_message("Something went wrong", session_id)
            await websocket.close()
            return
        while True:
            # Receives json as msg
            data = await websocket.receive_json()
            # data = await websocket.receive_text()
            user_text = data["payload"]["userInput"]["text"]
            print(f"User {user_id} sent: {user_text}")

            print("Message : ", data)
            # response_stream = await agent.arun(user_text, stream=True)
            response_stream =  agent.run(user_text, stream=True)
            print("response Stream :" ,response_stream)
            # p = Playground(agents=[agent])
            print(f"User: {user_id}, Session: {session_id}, Debug: {debug_mode}")
            print("Response stream:", response_stream)
            # resp_string = ""
            async for response in response_stream:
                if response.content:
                    await manager.send_personal_message(response.content, session_id)
            await manager.send_personal_message("[DONE]", session_id)

            #
            #     if not response.content == "":
            #         # await websocket.send_json({
            #         await manager.send_personal_message({
            #             "type": "new_message",
            #             "payload": {
            #                 "userInput": {
            #                     "role": "",
            #                     "text": ""
            #                 },
            #                 "message": response.content,
            #                 "gptText": response.content,
            #                 "from": "gpt",
            #                 "sent": str(response.created_at)
            #             }
            #         }, websocket)
            # await  manager.send_personal_message({
            #     "type": "new_message",
            #     "payload": {
            #         "userInput": {
            #             "role": "",
            #             "text": ""
            #         },
            #         "message": "[DONE]",
            #         "gptText": "[DONE]",
            #         "from": "gpt",
            #         "sent": ""
            #     }
            # }, websocket)

            # resp_string += response.content
        # print("Response String :: ", resp_string)
        # await websocket.send_text(f"RESP: {response_stream}")

    except WebSocketDisconnect:
        manager.disconnect(session_id)
        print(f"WebSocket connection closed for user {user_id}, session {session_id}")
