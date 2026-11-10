from typing import Literal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


class LogEntry(BaseModel):
    user: str
    action: str
    status: Literal["SUCCESS", "FAILED"]

app = FastAPI()

# In-memory database
database = [
    {"user": "alice", "action": "DeleteBucket", "status": "SUCCESS"},
    {"user": "bob", "action": "CreateBucket", "status": "FAILED"},
    {"user": "charlie", "action": "DeleteBucket", "status": "SUCCESS"}
]

# Endpoint 1: Get ALL logs
@app.get("/logs")
def get_all_logs():
    return database

# Endpoint 2: Get logs for a SPECIFIC user using a "Path Parameter"
@app.get("/logs/{username}")
def get_user_log(username: str):
    for entry in database:
        if entry["user"] == username:
            return entry

    raise HTTPException(status_code=404, detail=f"User '{username}' not found")

# Endpoint 3: Create a new log entry
@app.post("/logs", status_code=201)
def create_log(new_log: LogEntry):
    database.append(new_log.model_dump())
    return {"message": "Log entry created successfully", "log_entry": new_log.model_dump()}