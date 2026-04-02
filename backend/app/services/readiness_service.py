from app.utils.scoring import get_readiness_band

class ReadinessService:
    @staticmethod
    def get_national_summary(db):
        return {
            "national_score": 45.5,
            "band": "YELLOW",
            "red_counties": 3,
            "orange_counties": 8,
            "yellow_counties": 12,
            "green_counties": 2,
            "total_assessed_counties": 25
        }
    
    @staticmethod
    def get_region_readiness(db, region_id: str):
        return {
            "region_id": region_id,
            "readiness_score": 48.2,
            "readiness_band": "YELLOW",
            "affected_counties": 9,
            "assessments": 12
        }
