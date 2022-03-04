from fastapi import FastAPI, HTTPException
import uvicorn
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Todo(BaseModel):
  id: Optional[int] = 0
  value: str

todos = [
  {"id": 1, "value": "Hello"},
  {"id": 2, "value": "Bye"}
]

last_id = 2;

@app.get("/")
def read_root():
    return "Hello World"

@app.get("/todos")
def get_todos():
    return todos

@app.get("/todos/{id}")
def get_todo(id: int, q: str = None):
  todo = next((t for t in todos if t["id"] == id), None)
  if not todo:
    raise HTTPException(status_code = 404, detail="Todo not found")
  return todo

@app.post("/todos")
def create_todo(dto: Todo):
  todos.append({"id": last_id + 1, **dto})
  last_id += 1
  return dto

@app.put("/todos/{id}")
def update_todo(id: int, dto: Todo):
  todo = next((t for t in todos if t["id"] == id), None)
  if not todo:
    raise HTTPException(status_code = 404, detail="Todo not found")
  todo["value"] = dto.value
  return todo

@app.delete("/todos/{id}")
def delete_todo(id: int):
  todo = next((t for t in todos if t["id"] == id), None)
  if not todo:
    raise HTTPException(status_code = 404, detail="Todo not found")
  todos[:] = [i for i in todos if i["id"] != id]
  return {"id": id}

uvicorn.run(app,host="0.0.0.0",port="8080")