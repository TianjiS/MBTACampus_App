import os
import aiohttp
import asyncio
from datetime import datetime
from typing import List, Dict, Optional
from dotenv import load_dotenv

load_dotenv()

class MBTAClient:
    def __init__(self):
        self.api_key = os.getenv("MBTA_API_KEY", "c882eda42e27492c842907f4db7b0756")
        self.base_url = "https://api-v3.mbta.com"
        self.headers = {
            "x-api-key": self.api_key,
            "Accept": "application/vnd.api+json"
        }

    async def get_train_predictions(self, station_id: str) -> List[Dict]:
        """Get real-time predictions for a specific station"""
        async with aiohttp.ClientSession() as session:
            url = f"{self.base_url}/predictions"
            params = {
                "filter[stop]": station_id,
                "include": "trip,vehicle"
            }
            async with session.get(url, headers=self.headers, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("data", [])
                return []

    async def get_alerts(self, route_id: str = None) -> List[Dict]:
        """Get current MBTA alerts"""
        async with aiohttp.ClientSession() as session:
            url = f"{self.base_url}/alerts"
            params = {}
            if route_id:
                params["filter[route]"] = route_id
            async with session.get(url, headers=self.headers, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("data", [])
                return []

    async def get_station_info(self, station_id: str) -> Optional[Dict]:
        """Get detailed information about a specific station"""
        async with aiohttp.ClientSession() as session:
            url = f"{self.base_url}/stops/{station_id}"
            async with session.get(url, headers=self.headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("data")
                return None

    def is_rush_hour(self, station_name: str, current_time: datetime) -> bool:
        """Check if current time is rush hour for a specific station"""
        # This is a simplified version. In production, this should query the database
        # for the actual rush hour times for the station
        hour = current_time.hour
        if station_name in ["Babcock St", "Amory St"]:
            return (hour >= 9 and hour < 10) or (hour >= 12 and hour < 14) or (hour >= 17 and hour < 19)
        return False 