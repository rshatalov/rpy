from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
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