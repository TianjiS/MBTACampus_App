from datetime import datetime, timedelta
from typing import Dict, List, Optional
from .mbta_api import MBTAClient
from .database import Building, Station, get_db

class TripPlanner:
    def __init__(self):
        self.mbta_client = MBTAClient()
        self.db = next(get_db())

    async def get_building_suggestions(self, query: str) -> List[Dict]:
        """Get building suggestions based on partial name match"""
        buildings = self.db.query(Building).filter(
            Building.building_name.ilike(f"%{query}%")
        ).all()
        return [
            {
                "building_id": b.building_id,
                "building_name": b.building_name,
                "campus": b.campus,
                "closest_station": b.closest_station,
                "time_to_station": b.time_to_station
            }
            for b in buildings
        ]

    async def calculate_trip_time(
        self,
        building_id: int,
        target_time: datetime,
        direction: str
    ) -> Dict:
        """Calculate when to leave for the station based on current conditions"""
        building = self.db.query(Building).filter(Building.building_id == building_id).first()
        if not building:
            return {"error": "Building not found"}

        # Get station predictions
        station_predictions = await self.mbta_client.get_train_predictions(building.closest_station)
        
        # Get current alerts
        alerts = await self.mbta_client.get_alerts()
        
        # Check if it's rush hour
        is_rush = self.mbta_client.is_rush_hour(building.closest_station, datetime.now())
        
        # Calculate buffer time based on conditions
        buffer_time = building.time_to_station
        if is_rush:
            buffer_time += 5  # Add 5 minutes for rush hour
        if alerts:
            buffer_time += 3  # Add 3 minutes if there are alerts

        # Find the next train that arrives after the target time
        next_train = None
        for prediction in station_predictions:
            arrival_time = datetime.fromisoformat(prediction["attributes"]["arrival_time"])
            if arrival_time >= target_time:
                next_train = prediction
                break

        if not next_train:
            return {
                "error": "No trains available for the specified time",
                "suggestions": await self.get_alternative_stations(building_id)
            }

        # Calculate when to leave
        leave_time = next_train["attributes"]["arrival_time"] - timedelta(minutes=buffer_time)

        return {
            "building": building.building_name,
            "station": building.closest_station,
            "next_train": next_train["attributes"]["arrival_time"],
            "leave_by": leave_time,
            "buffer_time": buffer_time,
            "is_rush_hour": is_rush,
            "alerts": alerts,
            "suggestions": await self.get_alternative_stations(building_id) if is_rush else None
        }

    async def get_alternative_stations(self, building_id: int) -> List[Dict]:
        """Get alternative station suggestions during rush hour"""
        building = self.db.query(Building).filter(Building.building_id == building_id).first()
        if not building:
            return []

        # Get nearby stations (this is a simplified version)
        nearby_stations = self.db.query(Station).filter(
            Station.station_name != building.closest_station
        ).limit(3).all()

        return [
            {
                "station_name": station.station_name,
                "direction": station.direction,
                "estimated_walk_time": 15  # This should be calculated based on actual distances
            }
            for station in nearby_stations
        ] 