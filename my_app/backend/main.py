from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from backend.database import supabase


app = FastAPI(
    title="My Application API",
    version="1.0.0"
)


# -------------------------
# Schema
# -------------------------

class TaskCreate(BaseModel):
    title: str


# -------------------------
# Health Check
# -------------------------

@app.get("/")
def root():
    return {
        "message": "FastAPI backend is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


# -------------------------
# Get Tasks
# -------------------------

@app.get("/tasks")
def get_tasks():

    response = (
        supabase
        .table("tasks")
        .select("*")
        .order("id")
        .execute()
    )

    return response.data


# -------------------------
# Create Task
# -------------------------

@app.post("/tasks")
def create_task(task: TaskCreate):

    response = (
        supabase
        .table("tasks")
        .insert({
            "title": task.title,
            "completed": False
        })
        .execute()
    )

    return response.data


# -------------------------
# Delete Task
# -------------------------

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):

    response = (
        supabase
        .table("tasks")
        .delete()
        .eq("id", task_id)
        .execute()
    )

    if not response.data:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return {
        "message": "Task deleted",
        "data": response.data
    }