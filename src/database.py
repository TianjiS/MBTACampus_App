from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import os

# Create SQLite database
SQLALCHEMY_DATABASE_URL = "sqlite:///./mbtacampus.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Building(Base):
    __tablename__ = "buildings"

    building_id = Column(Integer, primary_key=True, index=True)
    building_name = Column(String, index=True)
    campus = Column(String)
    closest_station = Column(String)
    time_to_station = Column(Integer)  # in minutes

class Station(Base):
    __tablename__ = "stations"

    station_id = Column(Integer, primary_key=True, index=True)
    station_name = Column(String, unique=True, index=True)
    direction = Column(String)  # "Boston College" or "Government Center"

class RushHour(Base):
    __tablename__ = "rush_hours"

    id = Column(Integer, primary_key=True, index=True)
    day_of_week = Column(String)  # e.g., "Monday", "Tuesday", etc.
    start_time = Column(String)  # e.g., "09:30"
    end_time = Column(String)    # e.g., "10:10"
    station_name = Column(String)
    congestion_level = Column(Integer)  # scale 1-5

# Create all tables
Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 