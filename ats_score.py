def calculate_ats_score(detected_skills: list) -> int:
    """
    Simple ATS score heuristic based on number of detected skills.
    Adjust the scale/weights as needed.
    """
    if not detected_skills:
        return 0

    score = min(100, len(detected_skills) * 8)
    return score