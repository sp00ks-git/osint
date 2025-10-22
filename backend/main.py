from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import auth
import os
import json
from datetime import datetime

app = FastAPI()

# CORS configuration
origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# --- Directory setup ---
LOGS_DIR = "logs"
SNAPSHOTS_DIR = "snapshots"
os.makedirs(LOGS_DIR, exist_ok=True)
os.makedirs(SNAPSHOTS_DIR, exist_ok=True)
CONNECTIONS_LOG = os.path.join(LOGS_DIR, "connections.log")

class Token(BaseModel):
    access_token: str
    token_type: str

@app.post("/api/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = auth.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/api/session/start")
async def start_session(current_user: dict = Depends(auth.get_current_active_user)):
    with open(CONNECTIONS_LOG, "a") as f:
        log_entry = {
            "user": current_user["username"],
            "timestamp": datetime.utcnow().isoformat(),
            "event": "session_start",
        }
        f.write(json.dumps(log_entry) + "\n")
    return {"status": "session started"}

@app.get("/api/connection_logs")
async def get_connection_logs(current_user: dict = Depends(auth.get_current_active_user)):
    if not os.path.exists(CONNECTIONS_LOG):
        return []
    with open(CONNECTIONS_LOG, "r") as f:
        logs = [json.loads(line) for line in f]
    return logs

@app.post("/api/snapshots/upload")
async def upload_snapshot(current_user: dict = Depends(auth.get_current_active_user)):
    # This is a placeholder for the actual file upload logic
    return {"status": "snapshot uploaded"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
