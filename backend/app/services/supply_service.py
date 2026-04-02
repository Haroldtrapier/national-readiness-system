class SupplyService:
    @staticmethod
    def get_supply_package_for_hazard(db, hazard_code: str, severity_band: str):
        return {
            "package_id": "pkg_001",
            "package_name": "Emergency Response Package",
            "hazard_code": hazard_code,
            "severity_band": severity_band,
            "items": []
        }
