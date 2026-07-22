from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.core.websocket_manager import manager

router = APIRouter()


@router.websocket("/ws/meeting-status/{meeting_id}")
async def meeting_status_socket(websocket: WebSocket, meeting_id: int):
    await manager.connect(meeting_id, websocket)
    print(f"WebSocket connected for meeting {meeting_id}")
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        print(f"WebSocket disconnected (normal) for meeting {meeting_id}")
        manager.disconnect(meeting_id)
    except Exception as e:
        print(f"WebSocket error for meeting {meeting_id}: {e}")
        manager.disconnect(meeting_id)