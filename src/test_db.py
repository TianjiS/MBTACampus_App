from sqlalchemy.orm import Session
from database import engine, Building, Station, RushHour

def test_database():
    # Create a new session
    session = Session(bind=engine)
    
    try:
        # Test buildings table
        buildings = session.query(Building).all()
        print(f"\nFound {len(buildings)} buildings:")
        for building in buildings[:3]:  # Show first 3 buildings
            print(f"- {building.building_name} ({building.campus})")
        
        # Test stations table
        stations = session.query(Station).all()
        print(f"\nFound {len(stations)} stations:")
        for station in stations:
            print(f"- {station.station_name} ({station.direction})")
        
        # Test rush hours table
        rush_hours = session.query(RushHour).all()
        print(f"\nFound {len(rush_hours)} rush hour entries")
        
        return True
    except Exception as e:
        print(f"Error testing database: {str(e)}")
        return False
    finally:
        session.close()

if __name__ == "__main__":
    print("Testing database connection...")
    if test_database():
        print("\nDatabase connection successful!")
    else:
        print("\nDatabase connection failed!") 