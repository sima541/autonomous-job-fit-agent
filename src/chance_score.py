
def get_competition_factor(sector, title):
    title_lower = title.lower()
    
    if sector == "Government":
        return 0.5  # Bahut high competition
    elif "intern" in title_lower:
        return 0.9  # Internships thoda kam competitive hote hain
    elif any(word in title_lower for word in ["senior", "lead", "manager"]):
        return 1.1  # Senior roles mein fresher competition kam hota hai
    else:
        return 0.75  # Standard private-sector competition

def get_realistic_chance(match_score, sector, title):
    factor = get_competition_factor(sector, title)
    return match_score * factor