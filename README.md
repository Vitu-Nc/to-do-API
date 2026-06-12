# Todo API

A REST API built with FastAPI and Python.

## Features
- Create, read, update and delete todos
- Built with FastAPI and Pydantic
- UUID-based todo identification
- Auto-generated API documentation
  
## Authentication
- POST /register — create a new account (username + password)
- Passwords are hashed using bcrypt before storage
## Database
This API uses SQLite. The database file `todos.db` 
is created automatically when you run the server.

## Requirements
- Python 3.14+
- FastAPI
- Uvicorn

## Installation

1. Clone the repository
   -git clone https://github.com/Vitu-Nc/todo-api.git
2. Navigate into the folder
  -cd todo-api
3. Create a virtual environment
   -uv venv
4. Activate it
   -.venv\Scripts\activate
5. Install dependencies
   -uv pip install fastapi uvicorn
6.Running the API
-uvicorn main:app --reload


Then open http://127.0.0.1:8000/docs to test all endpoints.

 ## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /todos | Get all todos |
| POST | /todos | Create a new todo |
| GET | /todos/{id} | Get one todo |
| PUT | /todos/{id} | Update a todo |
| DELETE | /todos/{id} | Delete a todo |

## Example Request

POST /todos
```json
{
  "title": "Learn FastAPI",
  "description": "Build a todo API",
  "completed": false
}
```

## Tech Stack
- [FastAPI](https://fastapi.tiangolo.com/)
- [Pydantic](https://docs.pydantic.dev/)
- [Uvicorn](https://www.uvicorn.org/)
