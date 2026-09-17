from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from skills import extract_skills

model = SentenceTransformer('all-MiniLM-L6-v2')

# Dono resume versions load karo
with open('../data/resume_ds.txt', 'r', encoding='utf-8') as f:
    resume_ds = f.read()

with open('../data/resume_sde.txt', 'r', encoding='utf-8') as f:
    resume_sde = f.read()

# Job descriptions (abhi list mein, baad mein CSV/API se aayenge)
job_descriptions = [
    "We are hiring passed out BTech BE graduates from IT CS ECE Data science Position Associate Data Engineer Data Scientist Location Pune Skills Python SQL Cloud Data Engineering concepts Data Science Machine Learning concepts",
    "Software Engineering Intern BucketIn Comfortable writing code in at least one language JavaScript TypeScript C Sharp Python or Java Basic web fundamentals HTML CSS how HTTP requests work REST APIs Familiar with Git branches commits pull requests Curious about AI assisted development you have tried ChatGPT Copilot Claude or similar tools Willing to learn fast you will pick up React React Native or dotNet on the job Currently pursuing a degree in CS IT or related field",
]

def get_match_scores(resume, job_descriptions):
    resume_emb = model.encode([resume])
    jd_embs = model.encode(job_descriptions)
    scores = cosine_similarity(resume_emb, jd_embs)
    return scores[0]

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

def get_hybrid_score(resume, job_description):
    match_score = get_match_scores(resume, [job_description])[0]
    overlap_score = get_skill_overlap(resume, job_description)
    return (0.6 * match_score) + (0.4 * overlap_score)

def classify_fit(score):
    if score >= 0.40:
        return "Good Fit"
    elif score >= 0.28:
        return "Average Fit"
    else:
        return "Bad Fit"

def route_resume(job_description, confidence_threshold=0.05):
    """
    Har resume version ka hybrid score nikal ke, jo zyada score kare wahi version suggest karta hai.
    Agar scores bahut close hain, low confidence flag deta hai.
    """
    ds_score = get_hybrid_score(resume_ds, job_description)
    sde_score = get_hybrid_score(resume_sde, job_description)

    diff = abs(ds_score - sde_score)

    chosen = "DS-focused resume" if ds_score > sde_score else "SDE-focused resume"
    confidence = "Low Confidence" if diff < confidence_threshold else "High Confidence"

    return ds_score, sde_score, chosen, confidence

if __name__ == "__main__":
    for i, jd in enumerate(job_descriptions):
        ds_score, sde_score, chosen, confidence = route_resume(jd)
        print(f"\nJob {i+1}:")
        print(f"  DS Resume Score:  {ds_score:.4f} -> {classify_fit(ds_score)}")
        print(f"  SDE Resume Score: {sde_score:.4f} -> {classify_fit(sde_score)}")
        print(f"  Router Decision:  {chosen} ({confidence})")