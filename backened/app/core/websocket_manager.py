from fastapi import WebSocket
from typing import Dict, Optional
import asyncio


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, WebSocket] = {}
        # Reference to the MAIN server event loop (the one uvicorn runs on).
        # Background-task threads use this to schedule sends safely.
        self._loop: Optional[asyncio.AbstractEventLoop] = None

    async def connect(self, meeting_id: int, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[meeting_id] = websocket
        # connect() always runs on the main server loop — capture it here so a
        # background worker thread can later schedule sends onto THIS exact loop
        # (the loop that actually owns the websocket transport).
        self._loop = asyncio.get_running_loop()

    def disconnect(self, meeting_id: int):
        self.active_connections.pop(meeting_id, None)

    async def send_status(self, meeting_id: int, status: str):
        websocket = self.active_connections.get(meeting_id)
        if websocket is not None:
            await websocket.send_json({"status": status})

    def send_status_sync(self, meeting_id: int, status: str):
        """Send a status update from a synchronous / background-thread context.

        The LangGraph pipeline runs inside a FastAPI BackgroundTask, which
        executes sync functions in a threadpool worker thread that has NO event
        loop. The websocket, however, lives on the main server loop. So we must
        schedule the coroutine onto the main loop in a thread-safe way instead
        of spinning up a throwaway loop in the worker thread (which silently
        fails to deliver on the real connection).
        """
        loop = self._loop
        if loop is None or not loop.is_running():
            # No live server loop captured yet (nobody has connected) — there is
            # nothing we can safely send to.
            print(f"[ws] no running loop; dropping status '{status}' for meeting {meeting_id}")
            return

        # Are we already ON the main loop's thread? (Shouldn't happen with
        # BackgroundTasks, but stay safe — blocking on a future from within the
        # same loop would deadlock.)
        try:
            current = asyncio.get_running_loop()
        except RuntimeError:
            current = None

        if current is loop:
            asyncio.ensure_future(self.send_status(meeting_id, status))
            return

        # Normal path: we're on a worker thread. Schedule onto the main loop and
        # block briefly so statuses arrive in order and errors surface.
        future = asyncio.run_coroutine_threadsafe(
            self.send_status(meeting_id, status), loop
        )
        try:
            future.result(timeout=5)
        except Exception as e:
            print(f"[ws] failed to send status '{status}' for meeting {meeting_id}: {e}")


manager = ConnectionManager()
