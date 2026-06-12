from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import Field, Session, SQLModel, create_engine, select
from typing import Optional, List
from passlib.context import CryptContext
import uuid
#  DATABASE SETUP 
DATABASE_URL = "sqlite:///todos.db"
engine = create_engine(DATABASE_URL, echo=True)
def create_db():
    SQLModel.metadata.create_all(engine)
def get_session():
    with Session(engine) as session:
        yield session
#  MODELS 
class TodoBase(SQLModel):
    title: str
    description: Optional[str] = None
    completed: bool = False
class Todo(TodoBase, table=True):
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
class TodoCreate(TodoBase):
    pass
class TodoResponse(TodoBase):
    id: str
#  APP 
app = FastAPI(title="Simple Todo API")
@app.on_event("startup")
def on_startup():
    create_db()
#  ENDPOINTS 
@app.get("/todos", response_model=List[TodoResponse])
def get_todos(session: Session = Depends(get_session)):
    todos = session.exec(select(Todo)).all()
    return todos
@app.post("/todos", response_model=TodoResponse, status_code=201)
def create_todo(todo: TodoCreate, session: Session = Depends(get_session)):
    db_todo = Todo.model_validate(todo)
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo
@app.get("/todos/{todo_id}", response_model=TodoResponse)
def get_todo(todo_id: str, session: Session = Depends(get_session)):
    todo = session.get(Todo, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo
@app.put("/todos/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: str, updated: TodoCreate, session: Session = Depends(get_session)):
    todo = session.get(Todo, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    todo_data = updated.model_dump()
    for key, value in todo_data.items():
        setattr(todo, key, value)
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: str, session: Session = Depends(get_session)):
    todo = session.get(Todo, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    session.delete(todo)
    session.commit()
    return {"message": "Todo deleted successfully"}
# PASSWORD HASHING 
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def hash_password(password: str) -> str:
    return pwd_context.hash(password)
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
#  USER MODELS
class UserBase(SQLModel):
    username: str
class User(UserBase, table=True):
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    hashed_password: str
class UserCreate(UserBase):
    password: str
class UserResponse(UserBase):
    id: str
    
@app.post("/register", response_model=UserResponse, status_code=201)
def register(user: UserCreate, session: Session = Depends(get_session)):
    existing_user = session.exec(
        select(User).where(User.username == user.username)
    ).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_pw = hash_password(user.password)
    db_user = User(username=user.username, hashed_password=hashed_pw)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user
