from fastapi import WebSocket
from typing import Dict


class ConnectionManager:
    def __init__(self):
        # meeting_id -> WebSocket connection ka mapping
        self.active_connections: Dict[int, WebSocket] = {}

    async def connect(self, meeting_id: int, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[meeting_id] = websocket

    def disconnect(self, meeting_id: int):
        if meeting_id in self.active_connections:
            del self.active_connections[meeting_id]

    async def send_status(self, meeting_id: int, status: str):
        if meeting_id in self.active_connections:
            websocket = self.active_connections[meeting_id]
            await websocket.send_json({"status": status})


manager = ConnectionManager()