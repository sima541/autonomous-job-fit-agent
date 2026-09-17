# 🎯 Autonomous Job-Fit Agent

An AI-powered agent that autonomously fetches job postings, scores them against a resume using a hybrid NLP approach (semantic embeddings + skill-overlap), routes the best-matching resume version, and ranks results by a realistic chance-of-success score — across both private (live-fetched) and government (curated) job listings, and across multiple engineering branches.

Built as a personal project while job-hunting, to solve a real problem: manually reading through dozens of job descriptions and guessing which ones are actually worth applying to.

## 🔍 What it does

1. **Fetches live jobs** from the Adzuna API (private sector) and combines them with a curated dataset of real government job postings (SSC, UPSC, Railway, PSC, etc.)
2. **Scores each job** against a resume using a hybrid score: `0.6 × semantic similarity (Sentence-Transformers) + 0.4 × skill-overlap (Precision-Recall F1)`
3. **Routes to the best resume version** (if multiple are provided) with a confidence level
4. **Tags each job's sector** (Government / Private) and computes a **Realistic Chance Score** that factors in estimated competition level
5. **Explains every score** — shows which skills matched and which are missing
6. **Supports multiple engineering branches** (IT, Mechanical, Civil, Electrical) — not just tech resumes
7. **Surfaces a direct apply link** for each job (semi-automated — the agent finds and ranks, the user clicks to apply, respecting job portals' terms of service)
8. **Tracks applications** in a log with outcome status (Applied / Interviewed / Rejected) for future analysis
9. Runs entirely through a **Streamlit web UI** — upload any resume (PDF/DOCX/TXT), pick a branch, and get ranked results in seconds

## 🧠 Why hybrid scoring

Pure keyword matching (TF-IDF) misses synonyms ("ML" vs "Machine Learning"). Pure semantic embeddings alone struggled to distinguish "Average Fit" from "Bad Fit" cases. Combining both — validated against a manually-labeled ground truth set — gave the most reliable and explainable ranking (71% classification accuracy on the validation set).

## 🛠️ Tech Stack

- **NLP/ML:** Sentence-Transformers (`all-MiniLM-L6-v2`), scikit-learn (cosine similarity)
- **Backend:** Python, Pandas, class-based agent architecture
- **Data sources:** Adzuna Jobs API, curated government job dataset
- **File parsing:** pypdf, python-docx
- **UI:** Streamlit
- **Config:** python-dotenv for secrets management

## 📂 Project Structure

├── src/
│ ├── job_fit_agent.py # Main agent (class-based orchestrator)
│ ├── app.py # Streamlit UI
│ ├── skills.py # Multi-branch skill extraction + F1 overlap scoring
│ ├── fetch_jobs.py # Adzuna API integration
│ ├── government_jobs.py # Curated government jobs loader
│ ├── sector_tagger.py # Govt/Private sector detection
│ ├── chance_score.py # Realistic Chance Score heuristic
│ ├── outcome_tracker.py # Application logging
│ └── resume_reader.py # PDF/DOCX/TXT parsing
├── data/
│ ├── government_jobs.csv
│ ├── ground_truth.csv # Manually labeled validation set
│ └── ...
└── requirements.txt


## ⚠️ Honest Limitations

- The "Realistic Chance Score" competition factor is an assumption-based heuristic, not real applicant-count data
- Skill extraction uses a curated keyword list per branch, not fully dynamic keyword extraction
- Validated on a small (7-job) manually-labeled ground truth set — accuracy would benefit from a larger labeled dataset

## 🚀 Running locally

```bash
pip install -r requirements.txt
cd src
streamlit run app.py
```

You'll need an Adzuna API key (free at developer.adzuna.com) in a `.env` file:

ADZUNA_APP_ID=your_id
ADZUNA_APP_KEY=your_key
