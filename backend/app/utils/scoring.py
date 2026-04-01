from datetime import date


def hazard_score(
    probability: float,
    severity: float,
    exposure: float,
    vulnerability: float,
    confidence: float,
) -> float:
    score = (
        probability * 0.30
        + severity * 0.25
        + exposure * 0.20
        + vulnerability * 0.15
        + confidence * 0.10
    ) * 10
    return round(min(max(score, 0), 100), 2)


def readiness_band(score: float) -> str:
    if score >= 85:
        return "BLACK"
    if score >= 70:
        return "RED"
    if score >= 50:
        return "ORANGE"
    if score >= 30:
        return "YELLOW"
    return "GREEN"


def confidence_band(confidence: float) -> str:
    if confidence >= 0.7:
        return "HIGH"
    if confidence >= 0.4:
        return "MODERATE"
    return "LOW"


def shortage_score(required: float, available: float | None) -> float:
    available = available or 0.0
    if required <= 0:
        return 0.0
    shortage = max(required - available, 0)
    return round((shortage / required) * 100, 2)


def vendor_fit_score(
    item_match: float,
    geography_fit: float,
    capacity_fit: float,
    contract_fit: float,
    speed_fit: float,
    emergency_fit: float,
) -> float:
    return round(
        item_match * 0.25
        + geography_fit * 0.20
        + capacity_fit * 0.20
        + contract_fit * 0.15
        + speed_fit * 0.10
        + emergency_fit * 0.10,
        2,
    )


def it_replacement_score(
    purchase_date: date | None,
    warranty_end_date: date | None,
    security_gap: bool,
    critical_role: bool,
    lifecycle_years: int = 4,
) -> float:
    today = date.today()
    score = 0.0

    if purchase_date:
        age_years = (today - purchase_date).days / 365.25
        score += min(age_years / lifecycle_years, 1.0) * 40

    if warranty_end_date:
        warranty_days_left = (warranty_end_date - today).days
        if warranty_days_left < 0:
            score += 25
        elif warranty_days_left <= 90:
            score += 15
        elif warranty_days_left <= 180:
            score += 8

    if security_gap:
        score += 20
    if critical_role:
        score += 15

    return round(min(score, 100), 2)


def surge_device_quantity(
    staff_surge: int,
    shelter_count: int,
    eoc_activation: bool,
) -> dict[str, int]:
    laptops = max(staff_surge, 0)
    hotspots = max(round(staff_surge * 0.35), 2 if eoc_activation else 0)
    printers = max(shelter_count, 1 if eoc_activation else 0)
    tablets = shelter_count * 4
    monitors = round(laptops * 0.4)
    return {
        "laptops": laptops,
        "hotspots": hotspots,
        "printers": printers,
        "tablets": tablets,
        "monitors": monitors,
    }
