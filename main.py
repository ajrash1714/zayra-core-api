from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import os

app = FastAPI(
    title="Zayra ECG API",
    description="Core endpoints for ECG monitoring and patient management",
    version="1.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage
users_db = {}
events_db = {}
ingest_logs = []

# Models
class User(BaseModel):
    id: str
    name: str
    email: str
    age: int | None = None

class ECGData(BaseModel):
    user_id: str
    samples: list[float]
    sampling_rate: int = 250
    timestamp: str | None = None

class Event(BaseModel):
    id: str
    user_id: str
    event_type: str
    severity: str = "normal"
    description: str
    timestamp: str | None = None

# Health check
@app.get("/")
async def root():
    return {"status": "healthy", "service": "zayra-core-api"}

# Users endpoints
@app.get("/users")
async def get_users():
    """Get all registered users"""
    return {"users": list(users_db.values()), "count": len(users_db)}

@app.post("/users")
async def create_user(user: User):
    """Create a new user"""
    users_db[user.id] = user.dict()
    return {"status": "created", "user": users_db[user.id]}

@app.get("/users/{user_id}")
async def get_user(user_id: str):
    """Get a specific user by ID"""
    if user_id in users_db:
        return {"user": users_db[user_id]}
    return {"error": "User not found"}, 404

# ECG Data Ingestion
@app.post("/ingest")
async def ingest_ecg(data: ECGData):
    """Ingest ECG data from wearable device"""
    if data.timestamp is None:
        data.timestamp = datetime.utcnow().isoformat()
    
    ingest_logs.append({
        "user_id": data.user_id,
        "samples_count": len(data.samples),
        "sampling_rate": data.sampling_rate,
        "timestamp": data.timestamp
    })
    
    return {
        "status": "ingested",
        "user_id": data.user_id,
        "samples_received": len(data.samples),
        "message": "ECG data processed successfully"
    }

# Events endpoints
@app.get("/events")
async def get_events():
    """Get all recorded events"""
    return {"events": list(events_db.values()), "count": len(events_db)}

@app.post("/events")
async def create_event(event: Event):
    """Create a new cardiac event record"""
    if event.timestamp is None:
        event.timestamp = datetime.utcnow().isoformat()
    
    events_db[event.id] = event.dict()
    return {"status": "created", "event": events_db[event.id]}

@app.get("/events/{user_id}")
async def get_user_events(user_id: str):
    """Get events for a specific user"""
    user_events = [e for e in events_db.values() if e["user_id"] == user_id]
    return {"user_id": user_id, "events": user_events, "count": len(user_events)}

# Health and metrics
@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "zayra-core-api",
        "users": len(users_db),
        "events": len(events_db),
        "ingest_logs": len(ingest_logs)
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
