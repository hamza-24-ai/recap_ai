from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.core.websocket_manager import manager

router = APIRouter()


@router.websocket("/ws/meeting-status/{meeting_id}")
async def meeting_status_socket(websocket: WebSocket, meeting_id: int):
    await manager.connect(meeting_id, websocket)
    try:
        while True:
            # Connection ko khula rakhne ke liye — hum kuch receive nahi kar rahe abhi,
            # bas connection alive rakhne ke liye wait kar rahe hain
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(meeting_id)