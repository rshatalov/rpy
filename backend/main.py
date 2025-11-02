from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import get_db, Base, engine
from models import TestItem, Act, Tag, Question, StudySession, SessionQuestion
from pydantic import BaseModel, HttpUrl, field_validator
from datetime import date, datetime
from typing import Optional, List


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

class ActItemCreate(BaseModel):
    title: str = ""
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    parent_id: Optional[int] = None

    @field_validator('start_date', 'end_date')
    @classmethod
    def parse_dates(cls, v):
        if v == "" or v is None:
            return None
        return v
    
    @field_validator('parent_id')
    @classmethod
    def parse_parent_id(cls, v):
        if v == "" or v is None:
            return None
        return int(v)

class ActItemResponse(BaseModel):
    id: int
    title: str
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    parent_id: Optional[int] = None



class TagSchema(BaseModel):
    slug: str
    title: str
    class Config:
        from_attributes = True



class TestItemCreate(BaseModel):
    name: str
    description: str = ""

class TestItemResponse(BaseModel):
    id: int
    name: str
    description: str
    created_at: datetime


class QuestionCreate(BaseModel):
    q: str
    a: str
    difficulty: Optional[str] = None
    tag_slugs: List[str] = []  # Список slug'ов тегов

class QuestionResponse(BaseModel):
    id: int
    q: str
    a: str
    difficulty: Optional[str] = None
    tags: List[TagSchema] = []
    class Config:
        from_attributes = True

# Модели для учебных сессий
class StudySessionCreate(BaseModel):
    name: str
    description: Optional[str] = None

class StudySessionResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    start_date: datetime
    end_date: Optional[datetime] = None
    is_active: bool
    created_at: datetime
    class Config:
        from_attributes = True

class SessionQuestionResponse(BaseModel):
    id: int
    question_id: int
    times_shown: int
    last_shown: Optional[datetime] = None
    status: str
    question: QuestionResponse
    class Config:
        from_attributes = True

class QuestionRating(BaseModel):
    session_id: int
    question_id: int
    rating: str  # easy, medium, hard

@app.get("/")
async def root():
    return {"message": "Hello, World!"}


@app.get("/db-test/")
async def db_test(db: Session = Depends(get_db)):
    return {"message": "Database connected successfully"}


@app.get("/acts/")
async def get_acts(db: Session = Depends(get_db)):
    acts = db.query(Act).all()
    return acts

@app.post("/acts/", response_model=ActItemResponse)
async def create_act_item(act: ActItemCreate, db: Session = Depends(get_db)):
    db_item = Act(title=act.title, start_date=act.start_date, end_date=act.end_date, parent_id=act.parent_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@app.get("/acts/{act_id}")
async def get_act(act_id: int, db: Session = Depends(get_db)):
    act = db.query(Act).filter(Act.id == act_id).first()
    if act is None:
        raise HTTPException(status_code=404, detail="Act not found")
    return act





@app.get('/api/v1/tags/', response_model=list[TagSchema])
async def get_tags(db: Session = Depends(get_db)):
    tags = db.query(Tag).all()
    return tags

@app.get('/api/v1/tags/{tag_slug}', response_model=TagSchema)
async def get_tag(tag_slug: str, db: Session = Depends(get_db)):
    tag = db.query(Tag).filter(Tag.slug == tag_slug).first()
    if tag is None:
        raise HTTPException(status_code=404, detail='Tag not found')
    return tag

@app.post('/api/v1/tags/', response_model=TagSchema)
async def crate_tag(tag: TagSchema, db: Session = Depends(get_db)):
    existing_tag = db.query(Tag).filter(Tag.slug == tag.slug).first()
    if existing_tag:
        raise HTTPException(status_code=400, detail='Такой тэг уже существует')

    db_item = Tag(slug=tag.slug, title=tag.title)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@app.delete("/api/v1/tags/{tag_slug}")
async def delete_tag(tag_slug: str, db: Session = Depends(get_db)):
    db_tag = db.query(Tag).filter(Tag.slug == tag_slug).first()
    if db_tag is None:
        return HTTPException(status_code=404, detail='Такого тэга нет')

    db.delete(db_tag)
    db.commit()
    return {'message': 'Тэг успешно удалён'}



@app.get('/api/v1/questions/', response_model=list[QuestionResponse])
async def get_questions(db: Session = Depends(get_db)):
    qs = db.query(Question).all()
    return qs

@app.post("/api/v1/questions/", response_model=QuestionResponse)
async def create_question(question: QuestionCreate, db: Session = Depends(get_db)):
    db_question = Question(
        q=question.q,
        a=question.a,
        difficulty=question.difficulty
    )
    db.add(db_question)
    db.flush()  # Получаем ID

    if question.tag_slugs:
        for tag_slug in question.tag_slugs:
            tag = db.query(Tag).filter(Tag.slug == tag_slug).first()
            if tag:
                db_question.tags.append(tag)

    db.commit()
    db.refresh(db_question)
    return db_question



@app.put("/api/v1/questions/{question_id}", response_model=QuestionResponse)
async def update_question(question_id: int, question: QuestionCreate, db: Session = Depends(get_db)):
    try:
        # Находим вопрос
        db_question = db.query(Question).filter(Question.id == question_id).first()
        if not db_question:
            raise HTTPException(status_code=404, detail="Question not found")
        
        # Обновляем поля
        db_question.q = question.q
        db_question.a = question.a
        db_question.difficulty = question.difficulty
        
        # Очищаем старые теги
        db_question.tags.clear()
        
        # Добавляем новые теги
        if question.tag_slugs:
            for tag_slug in question.tag_slugs:
                tag = db.query(Tag).filter(Tag.slug == tag_slug).first()
                if tag:
                    db_question.tags.append(tag)
        
        db.commit()
        db.refresh(db_question)
        
        return {
            "id": db_question.id,
            "q": db_question.q,
            "a": db_question.a,
            "difficulty": db_question.difficulty,
            "tags": [{"slug": tag.slug, "title": tag.title} for tag in db_question.tags]
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Ошибка обновления вопроса: {str(e)}")



@app.delete("/api/v1/questions/{id}")
async def delete_question(id: int, db: Session = Depends(get_db)):
    q = db.query(Question).filter(Question.id == id).first()
    if q is None:
        return HTTPException(status_code=404, detail='Такого вопроса нет')

    db.delete(q)
    db.commit()
    return {'message': 'Вопрос успешно удалён'}






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

# API для учебных сессий
@app.post("/api/v1/study-sessions/", response_model=StudySessionResponse)
async def create_study_session(session: StudySessionCreate, db: Session = Depends(get_db)):
    """Создать новую учебную сессию"""
    db_session = StudySession(
        name=session.name,
        description=session.description
    )
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

@app.get("/api/v1/study-sessions/", response_model=List[StudySessionResponse])
async def get_study_sessions(db: Session = Depends(get_db)):
    """Получить все учебные сессии"""
    sessions = db.query(StudySession).all()
    return sessions

@app.get("/api/v1/study-sessions/{session_id}", response_model=StudySessionResponse)
async def get_study_session(session_id: int, db: Session = Depends(get_db)):
    """Получить учебную сессию по ID"""
    session = db.query(StudySession).filter(StudySession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Study session not found")
    return session

@app.delete("/api/v1/study-sessions/{session_id}")
async def delete_study_session(session_id: int, db: Session = Depends(get_db)):
    """Удалить учебную сессию"""
    session = db.query(StudySession).filter(StudySession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Study session not found")
    db.query(SessionQuestion).filter(SessionQuestion.session_id == session_id).delete()
    db.commit()
    db.delete(session)
    db.commit()
    return {"message": "Study session deleted"}


@app.post("/api/v1/study-sessions/{session_id}/end")
async def end_study_session(session_id: int, db: Session = Depends(get_db)):
    """Завершить учебную сессию"""
    session = db.query(StudySession).filter(StudySession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Study session not found")
    
    session.end_date = datetime.now()
    session.is_active = False
    db.commit()
    return {"message": "Study session ended"}

@app.get("/api/v1/study-sessions/{session_id}/next-question")
async def get_next_question(session_id: int, db: Session = Depends(get_db)):
    """Получить следующий вопрос для сессии"""
    session = db.query(StudySession).filter(StudySession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Study session not found")
    
    # Находим вопросы, которые еще не были показаны или показаны мало раз
    # Исключаем только те вопросы, которые помечены как "easy" (легкие)
    easy_question_ids = db.query(SessionQuestion.question_id).filter(
        SessionQuestion.session_id == session_id,
        SessionQuestion.status == 'easy'
    ).subquery()
    
    available_questions = db.query(Question).filter(
        ~Question.id.in_(easy_question_ids)
    ).all()
    
    if not available_questions:
        return {"message": "No more questions available"}
    
    # Выбираем случайный вопрос
    import random
    selected_question = random.choice(available_questions)
    
    # Добавляем или обновляем запись в сессии
    session_question = db.query(SessionQuestion).filter(
        SessionQuestion.session_id == session_id,
        SessionQuestion.question_id == selected_question.id
    ).first()
    
    if not session_question:
        session_question = SessionQuestion(
            session_id=session_id,
            question_id=selected_question.id,
            times_shown=1,
            last_shown=datetime.now()
        )
        db.add(session_question)
    else:
        session_question.times_shown += 1
        session_question.last_shown = datetime.now()
    
    db.commit()
    db.refresh(session_question)
    
    # Преобразуем вопрос в словарь для правильной сериализации
    question_data = {
        "id": selected_question.id,
        "q": selected_question.q,
        "a": selected_question.a,
        "difficulty": selected_question.difficulty,
        "tags": [{"slug": tag.slug, "title": tag.title} for tag in selected_question.tags]
    }
    
    return {
        "question": question_data,
        "session_question_id": session_question.id,
        "times_shown": session_question.times_shown
    }

@app.post("/api/v1/study-sessions/{session_id}/rate-question")
async def rate_question(session_id: int, rating: QuestionRating, db: Session = Depends(get_db)):
    """Оценить вопрос в сессии"""
    session_question = db.query(SessionQuestion).filter(
        SessionQuestion.session_id == session_id,
        SessionQuestion.question_id == rating.question_id
    ).first()
    
    if not session_question:
        raise HTTPException(status_code=404, detail="Question not found in session")
    
    session_question.status = rating.rating
    db.commit()
    
    return {"message": f"Question rated as {rating.rating}"}

@app.get("/api/v1/study-sessions/{session_id}/statistics")
async def get_session_statistics(session_id: int, db: Session = Depends(get_db)):
    """Получить статистику сессии"""
    session = db.query(StudySession).filter(StudySession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Study session not found")
    
    session_questions = db.query(SessionQuestion).filter(
        SessionQuestion.session_id == session_id
    ).all()
    
    total_questions = len(session_questions)
    easy_questions = len([sq for sq in session_questions if sq.status == 'easy'])
    medium_questions = len([sq for sq in session_questions if sq.status == 'medium'])
    hard_questions = len([sq for sq in session_questions if sq.status == 'hard'])
    pending_questions = len([sq for sq in session_questions if sq.status == 'pending'])
    
    total_shows = sum(sq.times_shown for sq in session_questions)
    
    return {
        "session": session,
        "total_questions": total_questions,
        "easy_questions": easy_questions,
        "medium_questions": medium_questions,
        "hard_questions": hard_questions,
        "pending_questions": pending_questions,
        "total_shows": total_shows,
        "average_shows": total_shows / total_questions if total_questions > 0 else 0
    }

