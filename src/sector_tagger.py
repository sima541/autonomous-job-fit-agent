GOVERNMENT_KEYWORDS = [
    "government", "public sector", "psu", "ssc", "upsc", "railway",
    "bank po", "civil services", "ministry", "sarkari"
]

def detect_sector(job_text):
    text = job_text.lower()
    for keyword in GOVERNMENT_KEYWORDS:
        if keyword in text:
            return "Government"
    return "Private"