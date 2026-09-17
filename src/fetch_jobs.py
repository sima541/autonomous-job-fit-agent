import requests
import os
from dotenv import load_dotenv

load_dotenv()

APP_ID = os.getenv("ADZUNA_APP_ID")
APP_KEY = os.getenv("ADZUNA_APP_KEY")

def fetch_jobs(keyword, num_results=10):
    url = "https://api.adzuna.com/v1/api/jobs/in/search/1"
    params = {
        "app_id": APP_ID,
        "app_key": APP_KEY,
        "results_per_page": num_results,
        "what": keyword
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data['results']

jobs = fetch_jobs("data scientist", num_results=10)

for i, job in enumerate(jobs, start=1):
    title = job['title']
    apply_link = job.get('redirect_url', 'Not available')
    company = job['company']['display_name']
    description = job['description']
    
    filename = f"../data/fetched_job_{i}.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"{title}\n{company}\n{apply_link}\n{description}")
    
    print(f"Saved: {filename} ({title} - {company})")