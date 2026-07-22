from fastapi import FastAPI
from app.core.database import Base,engine
from fastapi.security import OAuth2PasswordBearer

# Import all Routers
from app.routers import auth,meeting, project, decision, action_item,websocket


# Import all models 
from app.models.user import User
from app.models.project import Project
from app.models.meeting import Meeting
from app.models.decision import Decision
from app.models.agent_run_log import AgentRunLog
from app.models.action_item import ActionItem

# Decalre APP for api's

app = FastAPI(title="Recap_AI_MultiAgent_Automation")

# Get Token after login 
oauth_schema = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Declare all routers 
app.include_router(auth.router)
app.include_router(project.router)
app.include_router(meeting.router)
app.include_router(decision.router)
app.include_router(action_item.router)
app.include_router(websocket.router)



# Generate Tables in Supabase
Base.metadata.create_all(bind=engine)

# Link with frontened by cors method

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "message" : "Recap AI MultiAgent Automation API is running successfully"
    }