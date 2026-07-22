from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.meeting import Meeting
from app.core.cloudinary import upload_transcript, delete_transcript
from app.schemas.meeting import MeetingResponse
from app.core.security import get_current_user
from app.models.user import User

# Manageble into loder data by pass into function 
from app.services.file_extractor import extractor_text_from_file
# Get Starting Pipeline
from app.agents.graph import pipeline

router = APIRouter(prefix="/meetings", tags=["Meetings"])

ALLOWED_TYPES = [".txt", ".docx"]


# @router.post("/upload", response_model=MeetingResponse)
# async def upload_meeting(
#     project_id: int = Form(...),
#     title: str = Form(...),
#     file: UploadFile = File(...),
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user),
# ):
#     ext = "." + file.filename.split(".")[-1].lower()
#     if ext not in ALLOWED_TYPES:
#         raise HTTPException(status_code=400, detail="Only .txt and .docx files are allowed")

#     file_bytes = await file.read()

#     # Send data to extract_data_function
#     raw_text = extractor_text_from_file(file_bytes,file.filename)
#     # /////////////////////////////////////////////////////////

#     file_url, file_public_id = upload_transcript(file_bytes, file.filename)

#     new_meeting = Meeting(
#         project_id=project_id,
#         title=title,
#         file_url=file_url,
#         file_public_id=file_public_id,
#         status="processing",
#     )
#     db.add(new_meeting)
#     db.commit()
#     db.refresh(new_meeting)

#     # Agent pipeline trigger next step mein yahan add hoga
#     initial_state = {
#         "meeting_id": new_meeting.id,
#         "raw_transcript": raw_text,
#         "cleaned_transcript": "",
#         "decisions": [],
#         "action_items": [],
#     }

#     pipeline.invoke(initial_state)

#     db.refresh(new_meeting) # With done Status here 

#     return new_meeting

from fastapi import BackgroundTasks
import time
from app.core.database import Session_Local
from app.core.websocket_manager import manager


def run_pipeline_background(initial_state: dict):
    """Run the LangGraph pipeline in a background thread.

    A short delay gives the browser's WebSocket time to connect before the very
    first status ("cleaning_transcript") is emitted, so no early update is lost.
    On failure we mark the meeting "failed" and push an "error" status so the
    frontend loader unblocks instead of spinning forever.
    """
    meeting_id = initial_state.get("meeting_id")
    time.sleep(1)  # safety window for the WS handshake to complete
    try:
        pipeline.invoke(initial_state)
    except Exception as e:
        print(f"Pipeline failed for meeting {meeting_id}: {e}")
        try:
            db = Session_Local()
            meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
            if meeting:
                meeting.status = "failed"
                db.commit()
            db.close()
        except Exception as inner:
            print(f"Could not mark meeting {meeting_id} failed: {inner}")
        manager.send_status_sync(meeting_id, "error")


@router.post("/upload", response_model=MeetingResponse)
async def upload_meeting(
    background_tasks: BackgroundTasks,
    project_id: int = Form(...),
    title: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ext = "." + file.filename.split(".")[-1].lower()
    if ext not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="Only .txt and .docx files are allowed")

    file_bytes = await file.read()
    raw_text = extractor_text_from_file(file_bytes, file.filename)
    file_url, file_public_id = upload_transcript(file_bytes, file.filename)

    new_meeting = Meeting(
        project_id=project_id,
        title=title,
        file_url=file_url,
        file_public_id=file_public_id,
        status="processing",
    )
    db.add(new_meeting)
    db.commit()
    db.refresh(new_meeting)

    # Pipeline ko BACKGROUND mein chalao — turant response chala jayega
    initial_state = {
        "meeting_id": new_meeting.id,
        "raw_transcript": raw_text,
        "cleaned_transcript": "",
        "decisions": [],
        "action_items": [],
    }
    background_tasks.add_task(run_pipeline_background, initial_state)

    return new_meeting   # Ye TURANT return hoga, pipeline complete hone ka wait nahi karega


@router.delete("/{meeting_id}")
def delete_meeting(
    meeting_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")

    # Cloudinary se pehle delete karo (external store first — hamara established rule)
    if meeting.file_public_id:
        delete_transcript(meeting.file_public_id)

    # Phir DB row delete karo (cascade khud decisions/action_items hata dega)
    db.delete(meeting)
    db.commit()

    return {"message": "Meeting deleted successfully"}