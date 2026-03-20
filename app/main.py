from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import json
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()

# ---- Data Model ----
class Task(BaseModel):
    id: int
    title: str
    completed: bool = True


# ---- In-memory storage ----
tasks: List[Task] = []
templates = Jinja2Templates(directory="app/templates")

# ---- Root endpoint ----
@app.get("/")
def serve_ui(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# ---- Get all tasks ----
@app.get("/tasks")
def get_tasks():
    return tasks


# ---- Create new task ----
@app.post("/tasks")
def create_task(task: Task):
    tasks.append(task)
    return {"message": "Task added", "task": task}
#-----patch task as completed ----
@app.patch("/tasks/{task_id}")
def update_task(task_id: int):
    for i in range(len(tasks)):
        if tasks[i].id == task_id:
            tasks[i].completed = True
            return {"message": "Task updated"}
    return {"error": "Task not found"}


# ---- Delete task ----
@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            tasks.remove(task)
            return {"message": "Task deleted"}
    return {"error": "Task not found"}


# ---- Health check (important for DevOps later) ----
@app.get("/health")
def health():
    return {"status": "healthy"}
