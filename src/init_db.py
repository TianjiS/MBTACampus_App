import pandas as pd
from sqlalchemy.orm import Session
from .database import engine, Building, Station, RushHour
import os

def init_db():
    # Create tables
    from .database import Base
    Base.metadata.create_all(bind=engine)

    # Read CSV files
    buildings_df = pd.read_csv("buildings.csv")
    stations_df = pd.read_csv("stations.csv")
    rush_hours_df = pd.read_csv("rush_hours.csv")

    # Create database session
    session = Session(bind=engine)

    try:
        # Insert buildings
        for _, row in buildings_df.iterrows():
            building = Building(
                building_id=row["building_id"],
                building_name=row["building_name"],
                campus=row["campus"],
                closest_station=row["closest_station"],
                time_to_station=row["time_to_station"]
            )
            session.add(building)

        # Insert stations
        for _, row in stations_df.iterrows():
            station = Station(
                station_id=row["station_id"],
                station_name=row["station_name"],
                direction=row["direction"]
            )
            session.add(station)

        # Insert rush hours
        for _, row in rush_hours_df.iterrows():
            rush_hour = RushHour(
                day_of_week=row["day_of_week"],
                start_time=row["start_time"],
                end_time=row["end_time"],
                station_name=row["station_name"],
                congestion_level=row["congestion_level"]
            )
            session.add(rush_hour)

        session.commit()
        print("Database initialized successfully!")
    except Exception as e:
        session.rollback()
        print(f"Error initializing database: {str(e)}")
    finally:
        session.close()

if __name__ == "__main__":
    init_db() 