from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Dict
from .database import get_db
from .trip_planner import TripPlanner

router = APIRouter()
trip_planner = TripPlanner()

@router.get("/buildings/search")
async def search_buildings(query: str) -> List[Dict]:
    """Search for buildings by partial name match"""
    return await trip_planner.get_building_suggestions(query)

@router.get("/trip/calculate")
async def calculate_trip(
    building_id: int,
    target_time: datetime,
    direction: str
) -> Dict:
    """Calculate trip details including when to leave"""
    return await trip_planner.calculate_trip_time(building_id, target_time, direction)

@router.get("/stations")
async def get_stations(db: Session = Depends(get_db)) -> List[Dict]:
    """Get all stations"""
    stations = db.query(Station).all()
    return [
        {
            "station_id": s.station_id,
            "station_name": s.station_name,
            "direction": s.direction
        }
        for s in stations
    ]

@router.get("/alerts")
async def get_alerts(route_id: str = None) -> List[Dict]:
    """Get current MBTA alerts"""
    return await trip_planner.mbta_client.get_alerts(route_id)

@router.get("/predictions/{station_id}")
async def get_predictions(station_id: str) -> List[Dict]:
    """Get real-time predictions for a specific station"""
    return await trip_planner.mbta_client.get_train_predictions(station_id) 