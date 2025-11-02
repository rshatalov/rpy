from sqlalchemy import Column, Integer, Float, String, Date, DateTime, ForeignKey, Text, Table, Boolean, Enum
from sqlalchemy.sql import func
from database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr
import enum

class TestItem(Base):
    __tablename__ = "test_items"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class SortableMixin:

    @declared_attr
    def sort_order(cls):
        return Column(Integer, default=0, index=True)
    

class Act(SortableMixin, Base):
    __tablename__ = "acts"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)
    hidden = Column(Boolean, default=False)
    parent_id = Column(Integer, ForeignKey('acts.id'), nullable=True)
    parent = relationship("Act", remote_side=[id], backref="children")
    tasks = relationship("Task", back_populates="act")
    notes = relationship("ActNote", back_populates="act")
    times = relationship("Time", back_populates="act")
    timers = relationship("Timer", back_populates="act") 

class Plan(SortableMixin, Base):
    __tablename__ = "plans"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)
    parent_id = Column(Integer, ForeignKey('plans.id'), nullable=True)
    parent = relationship("Plan", remote_side=[id], backref='children')
    tasks = relationship("Task", back_populates="plan") 
    notes = relationship("PlanNote", back_populates="plan")

class Task(SortableMixin, Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(Text)
    start_date = Column(DateTime(timezone=True))
    end_date = Column(DateTime(timezone=True))
    plan_id = Column(Integer, ForeignKey('plans.id'), nullable=True)
    plan = relationship("Plan", back_populates="tasks")
    act_id = Column(Integer, ForeignKey('acts.id'), nullable=True)
    act = relationship("Act", back_populates="tasks")

class PlanNote(Base):
    __tablename__ = "plan_notes"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    content = Column(Text)
    plan_id = Column(Integer, ForeignKey('plans.id'), nullable=True)
    plan = relationship("Plan", back_populates="notes")

class ActNote(Base):
    __tablename__ = "act_notes"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    content = Column(Text)
    act_id = Column(Integer, ForeignKey('acts.id'), nullable=True)
    act = relationship("Act", back_populates="notes")

class Time(Base):
    __tablename__ = "times"

    day = Column(Date, primary_key=True)
    act_id = Column(Integer, ForeignKey('acts.id'), primary_key=True)
    time = Column(Integer, default=0)
    count = Column(Float, default=0)
    act = relationship("Act", back_populates="times")


class TimerState(enum.Enum):
    STOPPED = "stopped"
    COUNTING = "counting"
    PAUSED = "paused"

class Timer(Base):
    __tablename__ = "timers"

    id = Column(Integer, primary_key=True, index=True)
    time = Column(Integer, default=0)
    start_time = Column(DateTime(timezone=True), server_default=func.now())
    act_id = Column(Integer, ForeignKey('acts.id'), nullable=True)
    act = relationship("Act", back_populates="timers")
    state = Column(Enum(TimerState), default=TimerState.STOPPED, nullable=False)


question_tags = Table(
    'question_tags',
    Base.metadata,
    Column('question_id', Integer, ForeignKey('questions.id'), primary_key=True),
    Column('tag_slug', String, ForeignKey('tags.slug'), primary_key=True)
)

class Tag(Base):
    __tablename__ = 'tags'

    slug = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)

    questions = relationship("Question", secondary=question_tags, back_populates="tags")

class Question(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True, index=True)
    q = Column(Text, nullable=False)
    a = Column(Text, nullable=False)
    difficulty = Column(String(20), nullable=True)

    tags = relationship("Tag", secondary=question_tags, back_populates="questions")
    session_questions = relationship("SessionQuestion", back_populates="question")

class StudySession(Base):
    __tablename__ = 'study_sessions'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    start_date = Column(DateTime(timezone=True), server_default=func.now())
    end_date = Column(DateTime(timezone=True), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    session_questions = relationship("SessionQuestion", back_populates="session")

class SessionQuestion(Base):
    __tablename__ = 'session_questions'

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey('study_sessions.id'), nullable=False)
    question_id = Column(Integer, ForeignKey('questions.id'), nullable=False)
    times_shown = Column(Integer, default=0)
    last_shown = Column(DateTime(timezone=True), nullable=True)
    status = Column(String(20), default='pending')  # pending, easy, medium, hard
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    session = relationship("StudySession", back_populates="session_questions")
    question = relationship("Question", back_populates="session_questions")

