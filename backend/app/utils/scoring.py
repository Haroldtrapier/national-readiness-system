def calculate_hazard_score(probability=0.5, severity=0.5, exposure=0.5, vulnerability=0.5, confidence=0.8):
    score = ((probability * 0.30) + (severity * 0.25) + (exposure * 0.20) + (vulnerability * 0.15) + (confidence * 0.10)) * 10
    return round(min(100, max(0, score)), 2)

def get_readiness_band(hazard_score):
    if hazard_score < 30:
        return "GREEN"
    elif hazard_score < 50:
        return "YELLOW"
    elif hazard_score < 70:
        return "ORANGE"
    elif hazard_score < 85:
        return "RED"
    else:
        return "BLACK"
