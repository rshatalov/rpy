from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import get_db, Base, engine
from models import TestItem
from pydantic import BaseModel
from datetime import datetime


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173",
                   "http://localhost:3000", "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TestItemCreate(BaseModel):
    name: str
    description: str = ""

class TestItemResponse(BaseModel):
    id: int
    name: str
    description: str
    created_at: datetime



@app.get("/")
async def root():
    return {"message": "Hello, World!"}


@app.get("/db-test/")
async def db_test(db: Session = Depends(get_db)):
    return {"message": "Database connected successfully"}


@app.post("/test-items/", response_model=TestItemResponse)
async def create_test_item(item: TestItemCreate, db: Session = Depends(get_db)):
    db_item = TestItem(name=item.name, description=item.description)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# Эндпоинт для получения всех записей
@app.get("/test-items/")
async def get_test_items(db: Session = Depends(get_db)):
    items = db.query(TestItem).all()
    return items

# Эндпоинт для получения записи по ID
@app.get("/test-items/{item_id}")
async def get_test_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(TestItem).filter(TestItem.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.get("/db/inspect")
async def inspect_db(db: Session = Depends(get_db)):
    # Показать все таблицы
    tables = db.execute(text("SELECT name FROM sqlite_master WHERE type='table';")).fetchall()
    

    result = {}
    for table in tables:
        table_name = table[0]
        data = db.execute(text(f"SELECT * FROM {table_name};")).fetchall()
        result[table_name] = [dict(row._mapping) for row in data]
    
    return result


@app.get("/{id:str}/")
async def get_id(id: str):
    return {"id": id}


@app.get("/activities/{slug:str}/")
async def activity(slug: str):
    return {"slug": slug}
