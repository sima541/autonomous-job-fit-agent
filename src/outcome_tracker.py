import pandas as pd
import os
from datetime import date

LOG_FILE = '../data/applications_log.csv'

def log_application(job_id, job_title, sector, hybrid_score, realistic_chance, resume_used, outcome="Applied"):
    df = pd.read_csv(LOG_FILE)
    
    if job_id in df['job_id'].values:
        print(f"Job_id {job_id} already logged, skipping.")
        return
    
    new_entry = {
        "job_id": job_id,
        "job_title": job_title,
        "sector": sector,
        "hybrid_score": hybrid_score,
        "realistic_chance": realistic_chance,
        "resume_used": resume_used,
        "applied_date": date.today().isoformat(),
        "outcome": outcome
    }
    
    df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    df.to_csv(LOG_FILE, index=False)
    print(f"Logged: {job_title} -> {outcome}")
def update_outcome(job_id, new_outcome):
    df = pd.read_csv(LOG_FILE)
    df.loc[df['job_id'] == job_id, 'outcome'] = new_outcome
    df.to_csv(LOG_FILE, index=False)
    print(f"Updated job_id {job_id} -> {new_outcome}")

if __name__ == "__main__":
    log_application(
        job_id=1,
        job_title="Data Scientist at Atain",
        sector="Private",
        hybrid_score=0.3109,
        realistic_chance=0.2332,
        resume_used="DS-focused",
        outcome="Applied"
    )
    update_outcome(job_id=1, new_outcome="Interviewed")