from fetch_jobs import fetch_jobs
from sector_tagger import detect_sector
from skills import extract_skills, get_matching_keywords
from chance_score import get_realistic_chance
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from datetime import date
from government_jobs import load_government_jobs

class JobFitAgent:
    def __init__(self, resume_ds_path, resume_sde_path):
        with open(resume_ds_path, 'r', encoding='utf-8') as f:
            self.resume_ds = f.read()
        
        with open(resume_sde_path, 'r', encoding='utf-8') as f:
            self.resume_sde = f.read()
        
        print("Agent initialized with both resume versions.")
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.history = []

    def get_hybrid_score(self, resume, job_description, branch="IT/Computer Science"):
        resume_emb = self.model.encode([resume])
        jd_emb = self.model.encode([job_description])
        embedding_score = cosine_similarity(resume_emb, jd_emb)[0][0]
        
        resume_skills = set(extract_skills(resume, branch))
        jd_skills = set(extract_skills(job_description, branch))
        
        if len(jd_skills) == 0 or len(resume_skills) == 0:
            overlap_score = 0.0
        else:
            matched = resume_skills.intersection(jd_skills)
            precision = len(matched) / len(resume_skills)
            recall = len(matched) / len(jd_skills)
            overlap_score = 0.0 if (precision + recall == 0) else 2 * (precision * recall) / (precision + recall)
        
        return (0.6 * embedding_score) + (0.4 * overlap_score)

    def route_resume(self, job_description, branch="IT/Computer Science", confidence_threshold=0.05):
        ds_score = self.get_hybrid_score(self.resume_ds, job_description, branch)
        sde_score = self.get_hybrid_score(self.resume_sde, job_description, branch)
        
        diff = abs(ds_score - sde_score)
        chosen = "DS-focused" if ds_score > sde_score else "SDE-focused"
        confidence = "Low" if diff < confidence_threshold else "High"
        
        best_score = max(ds_score, sde_score)
        return best_score, chosen, confidence

    def classify_fit(self, score):
        if score >= 0.40:
            return "Good Fit"
        elif score >= 0.28:
            return "Average Fit"
        else:
            return "Bad Fit"

    def run(self, keyword="data scientist", num_results=10, branch="IT/Computer Science"):
        print(f"\nAgent starting: searching for '{keyword}' jobs...\n")
        jobs = fetch_jobs(keyword, num_results)

        govt_jobs_raw = load_government_jobs()
        govt_jobs = []
        for gj in govt_jobs_raw:
            govt_jobs.append({
                "title": gj["job_title"],
                "company": gj["department"],
                "description": gj["description"],
                "redirect_url": "Government portal — apply via official website"
            })

        jobs = jobs + govt_jobs

        results = []
        for job in jobs:
            title = job['title']
            
            if isinstance(job['company'], dict):
                company = job['company']['display_name']
            else:
                company = job['company']
            
            description = job['description']
            apply_link = job.get('redirect_url', 'Not available')
            
            score, resume_choice, confidence = self.route_resume(description, branch)
            sector = "Government" if apply_link == "Government portal — apply via official website" else detect_sector(description)
            chance = get_realistic_chance(score, sector, title)
            matched, missing = get_matching_keywords(
                self.resume_ds if resume_choice == "DS-focused" else self.resume_sde,
                description,
                branch
            )
            
            entry = {
                "title": title, "company": company, "sector": sector,
                "score": score, "chance": chance, "resume_choice": resume_choice,
                "confidence": confidence, "matched": matched, "missing": missing,
                "apply_link": apply_link
            }
            results.append(entry)
            self.history.append(entry)
        
        results.sort(key=lambda x: x['chance'], reverse=True)
        return results
    def run_with_resume(self, resume_text, keyword="data scientist", num_results=10, branch="IT/Computer Science"):
        print(f"\nAgent starting: searching for '{keyword}' jobs...\n")
        jobs = fetch_jobs(keyword, num_results)

        govt_jobs_raw = load_government_jobs()
        govt_jobs = []
        for gj in govt_jobs_raw:
            govt_jobs.append({
                "title": gj["job_title"],
                "company": gj["department"],
                "description": gj["description"],
                "redirect_url": "Government portal — apply via official website"
            })

        jobs = jobs + govt_jobs

        results = []
        for job in jobs:
            title = job['title']
            company = job['company']['display_name'] if isinstance(job['company'], dict) else job['company']
            description = job['description']
            apply_link = job.get('redirect_url', 'Not available')
            
            score = self.get_hybrid_score(resume_text, description, branch)
            sector = "Government" if apply_link == "Government portal — apply via official website" else detect_sector(description)
            chance = get_realistic_chance(score, sector, title)
            matched, missing = get_matching_keywords(resume_text, description, branch)
            
            entry = {
                "title": title, "company": company, "sector": sector,
                "score": score, "chance": chance, "fit": self.classify_fit(score),
                "matched": matched, "missing": missing, "apply_link": apply_link
            }
            results.append(entry)
        
        results.sort(key=lambda x: x['chance'], reverse=True)
        return results
if __name__ == "__main__":
    agent = JobFitAgent('../data/resume_ds.txt', '../data/resume_sde.txt')
    results = agent.run(keyword="data scientist", num_results=10, branch="IT/Computer Science")
    
    print(f"\n=== Agent Results — {date.today().isoformat()} ===\n")
    for i, r in enumerate(results, start=1):
        print(f"{i}. {r['title']} at {r['company']} [{r['sector']}]")
        print(f"   Resume: {r['resume_choice']} (Confidence: {r['confidence']})")
        print(f"   Realistic Chance: {r['chance']:.4f}")
        print(f"   ✓ Matched: {', '.join(r['matched']) if r['matched'] else 'None'}")
        print(f"   ✗ Missing: {', '.join(r['missing']) if r['missing'] else 'None'}")
        print(f"   Apply here: {r['apply_link']}")
        print()