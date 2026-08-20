from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from backend.database import supabase


app = FastAPI(
    title="My Application API",
    version="1.0.0"
)


# -------------------------
# Schemas
# -------------------------

class TaskCreate(BaseModel):
    title: str


class TaskUpdate(BaseModel):
    completed: Optional[bool] = None
    title: Optional[str] = None


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
# Update Task
# -------------------------

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: TaskUpdate):

    update_data = {}
    if task.completed is not None:
        update_data["completed"] = task.completed
    if task.title is not None:
        update_data["title"] = task.title

    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="No fields provided for update"
        )

    response = (
        supabase
        .table("tasks")
        .update(update_data)
        .eq("id", task_id)
        .execute()
    )

    if not response.data:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
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