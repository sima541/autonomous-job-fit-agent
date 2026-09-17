from fetch_jobs import fetch_jobs
from sector_tagger import detect_sector
from skills import extract_skills, get_matching_keywords
from embeddings import get_hybrid_score, classify_fit
from chance_score import get_realistic_chance
from datetime import date

with open('../data/my_resume.txt', 'r', encoding='utf-8') as f:
    resume_text = f.read()

def generate_digest(keyword="data scientist", num_results=10):
    jobs = fetch_jobs(keyword, num_results)
    
    digest_entries = []
    for job in jobs:
        title = job['title']
        company = job['company']['display_name']
        description = job['description']
        
        hybrid_score = get_hybrid_score(resume_text, description)
        sector = detect_sector(description)
        realistic_chance = get_realistic_chance(hybrid_score, sector, title)
        
        digest_entries.append({
            "title": title,
            "company": company,
            "sector": sector,
            "score": hybrid_score,
            "chance": realistic_chance
        })
    
    digest_entries.sort(key=lambda x: x['chance'], reverse=True)
    return digest_entries

if __name__ == "__main__":
    entries = generate_digest()
    
    print(f"=== Daily Job Digest — {date.today().isoformat()} ===\n")
    
    for i, entry in enumerate(entries[:5], start=1):
        print(f"{i}. {entry['title']} at {entry['company']} [{entry['sector']}]")
        print(f"   Realistic Chance: {entry['chance']:.4f} ({classify_fit(entry['score'])})")
        print()