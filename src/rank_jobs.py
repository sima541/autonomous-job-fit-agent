import os
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from skills import extract_skills
from sector_tagger import detect_sector
from chance_score import get_realistic_chance
from skills import get_matching_keywords

model = SentenceTransformer('all-MiniLM-L6-v2')

with open('../data/my_resume.txt', 'r', encoding='utf-8') as f:
    resume_text = f.read()

def get_match_score(resume, job_description):
    resume_emb = model.encode([resume])
    jd_emb = model.encode([job_description])
    return cosine_similarity(resume_emb, jd_emb)[0][0]

def get_skill_overlap(resume, job_description):
    resume_skills = set(extract_skills(resume))
    jd_skills = set(extract_skills(job_description))
    if len(jd_skills) == 0 or len(resume_skills) == 0:
        return 0.0
    matched = resume_skills.intersection(jd_skills)
    precision = len(matched) / len(resume_skills)
    recall = len(matched) / len(jd_skills)
    if precision + recall == 0:
        return 0.0
    return 2 * (precision * recall) / (precision + recall)

results = []

for i in range(1, 11):
    filename = f"../data/fetched_job_{i}.txt"
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    title = lines[0]
    company = lines[1] if len(lines) > 1 else "Unknown"
    
    match_score = get_match_score(resume_text, content)
    overlap_score = get_skill_overlap(resume_text, content)
    hybrid_score = (0.6 * match_score) + (0.4 * overlap_score)
    sector = detect_sector(content)
    realistic_chance = get_realistic_chance(hybrid_score, sector, title)
    matched_skills, missing_skills = get_matching_keywords(resume_text, content)
    results.append((title, company, sector, hybrid_score, realistic_chance, matched_skills, missing_skills))

# Best match se worst match tak sort karo
results.sort(key=lambda x: x[4], reverse=True)

print("Ranked Jobs by Realistic Chance (best first):\n")
for rank, (title, company, sector, score, chance, matched, missing) in enumerate(results, start=1):
    print(f"{rank}. {title} at {company} [{sector}]")
    print(f"   Match: {score:.4f} | Realistic Chance: {chance:.4f}")
    print(f"   ✓ Matching skills: {', '.join(matched) if matched else 'None'}")
    print(f"   ✗ Missing skills: {', '.join(missing) if missing else 'None'}")
    print()