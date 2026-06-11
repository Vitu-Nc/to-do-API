from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uuid

app = FastAPI(title="Simple Todo API")

# Home Route
@app.get("/")
async def home():
    return {
        "message": "Welcome to the Simple Todo API",
        "docs": "/docs"
    }

# In-memory storage
todos = {}

# Pydantic model for request/response
class Todo(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

class TodoResponse(Todo):
    id: str

# Getting  all todos
@app.get("/todos", response_model=List[TodoResponse])
async def get_todos():
    return list(todos.values())

# Creating a todo
@app.post("/todos", response_model=TodoResponse, status_code=201)
async def create_todo(todo: Todo):
    todo_id = str(uuid.uuid4())

    todo_dict = todo.model_dump()
    todo_dict["id"] = todo_id

    todos[todo_id] = todo_dict

    return todo_dict

# Geting a single todo
@app.get("/todos/{todo_id}", response_model=TodoResponse)
async def get_todo(todo_id: str):
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail="Todo not found")

    return todos[todo_id]

# Update a todo
@app.put("/todos/{todo_id}", response_model=TodoResponse)
async def update_todo(todo_id: str, todo: Todo):
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail="Todo not found")

    todo_dict = todo.model_dump()
    todo_dict["id"] = todo_id

    todos[todo_id] = todo_dict

    return todo_dict

# Delete a todo
@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: str):
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail="Todo not found")

    del todos[todo_id]

    return {"message": "Todo deleted successfully"}