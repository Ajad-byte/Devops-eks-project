from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

# ---- Data Model ----
class Task(BaseModel):
    id: int
    title: str
    completed: bool = False


# ---- In-memory storage ----
tasks: List[Task] = []


# ---- Root endpoint ----
@app.get("/")
def home():
    return {"message": "Task Manager API Running"}


# ---- Get all tasks ----
@app.get("/tasks")
def get_tasks():
    return tasks


# ---- Create new task ----
@app.post("/tasks")
def create_task(task: Task):
    tasks.append(task)
    return {"message": "Task added", "task": task}


# ---- Delete task ----
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            tasks.remove(task)
            return {"message": "Task deleted"}
    return {"error": "Task not found"}


# ---- Health check (important for DevOps later) ----
@app.get("/health")
def health():
    return {"status": "healthy"}
