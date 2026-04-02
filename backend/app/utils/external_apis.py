import httpx
import asyncio
from typing import List, Dict
from datetime import datetime, timedelta

class NWSClient:
    BASE_URL = "https://api.weather.gov"
    
    @staticmethod
    async def get_active_alerts() -> List[Dict]:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{NWSClient.BASE_URL}/alerts/active?point=35.0,-97.0")
                data = response.json()
                alerts = []
                for feature in data.get("features", []):
                    alerts.append({
                        "id": feature["id"],
                        "event": feature["properties"].get("event"),
                        "headline": feature["properties"].get("headline"),
                        "severity": feature["properties"].get("severity"),
                    })
                return alerts
        except:
            return []

class USGSClient:
    BASE_URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"
    
    @staticmethod
    async def get_recent_earthquakes(hours_back=24) -> List[Dict]:
        try:
            end_time = datetime.utcnow()
            start_time = end_time - timedelta(hours=hours_back)
            
            params = {
                "format": "geojson",
                "starttime": start_time.isoformat(),
                "endtime": end_time.isoformat(),
                "minmagnitude": 2.5,
                "orderby": "time-asc"
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get(USGSClient.BASE_URL, params=params)
                data = response.json()
                
                earthquakes = []
                for feature in data.get("features", []):
                    props = feature["properties"]
                    coords = feature["geometry"]["coordinates"]
                    earthquakes.append({
                        "id": feature["id"],
                        "magnitude": props.get("mag"),
                        "place": props.get("place"),
                    })
                return earthquakes
        except:
            return []
