from sqlalchemy import Column,Integer, String, Text, DateTime, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime

SQLALCHEMY_DATABASE_URL = "sqlite:///./radiology.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL,connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit = False)
Base = declarative_base()

#model
class RadiologyRecord(Base):
    __tablename__ = "radiology_records"

    id = Column(Integer, primary_key=True)
    patient_id = Column(String)
    image_filename = Column(String)
    Diagnosis = Column(Text)
    timestamp = Column(DateTime, default= datetime.utcnow)

Base.metadata.create_all(bind = engine)

