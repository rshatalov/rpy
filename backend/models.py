from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Text, Table
from sqlalchemy.sql import func
from database import Base
from sqlalchemy.orm import relationship

class TestItem(Base):
    __tablename__ = "test_items"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Act(Base):
    __tablename__ = "acts"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)
    parent_id = Column(Integer, ForeignKey('acts.id'), nullable=True)
    parent = relationship("Act", remote_side=[id], backref="children")


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

