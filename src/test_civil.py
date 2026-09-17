from skills import get_matching_keywords

with open('../data/resume_civil.txt', 'r', encoding='utf-8') as f:
    civil_resume = f.read()

# Ek sample Civil job description (SSC JE Civil wala, jo humare government_jobs.csv mein bhi hai)
civil_jd = "Junior Engineer recruitment for civil works including site supervision quantity surveying structural design and construction management"

matched, missing = get_matching_keywords(civil_resume, civil_jd, branch="Civil")

print("Matched skills:", matched)
print("Missing skills:", missing)