import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from skills import extract_skills, SKILL_LIST

model = SentenceTransformer('all-MiniLM-L6-v2')

# Resume load karo
with open('../data/my_resume.txt', 'r', encoding='utf-8') as f:
    resume_text = f.read()

# Ground truth table load karo
ground_truth = pd.read_csv('../data/ground_truth.csv')

def get_match_score(resume, job_description):
    resume_emb = model.encode([resume])
    jd_emb = model.encode([job_description])
    score = cosine_similarity(resume_emb, jd_emb)
    return score[0][0]

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
    
    f1 = 2 * (precision * recall) / (precision + recall)
    return f1

def classify_fit(score):
    if score >= 0.40:
        return "Good Fit"
    elif score >= 0.28:
        return "Average Fit"
    else:
        return "Bad Fit"

# Har job_id ke liye uski JD file padho aur score nikalo
match_scores = []
overlap_scores = []
hybrid_scores = []

for job_id in ground_truth['job_id']:
    with open(f'../data/job_{job_id}.txt', 'r', encoding='utf-8') as f:
        jd_text = f.read()
    
    match_score = get_match_score(resume_text, jd_text)
    overlap_score = get_skill_overlap(resume_text, jd_text)
    hybrid_score = (0.6 * match_score) + (0.4 * overlap_score)
    
    match_scores.append(match_score)
    overlap_scores.append(overlap_score)
    hybrid_scores.append(hybrid_score)

ground_truth['embedding_score'] = match_scores
ground_truth['skill_overlap'] = overlap_scores
ground_truth['hybrid_score'] = hybrid_scores
ground_truth['predicted_label'] = ground_truth['hybrid_score'].apply(classify_fit)

pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

print(ground_truth[['job_title', 'fit_label', 'hybrid_score', 'predicted_label']])

print("\nAverage hybrid score by fit label:")
print(ground_truth.groupby('fit_label')['hybrid_score'].mean())

correct = (ground_truth['fit_label'] == ground_truth['predicted_label']).sum()
total = len(ground_truth)
print(f"\nAccuracy: {correct}/{total} = {correct/total:.2%}")