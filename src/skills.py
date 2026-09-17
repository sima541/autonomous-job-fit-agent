import re
SKILL_LISTS = {
    "IT/Computer Science": [
        "python", "sql", "java", "javascript", "c++", "c",
        "machine learning", "deep learning", "nlp", "data science",
        "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch",
        "react", "react native", "node.js", "express.js", "next.js",
        "html", "css", "rest api", "fastapi", "django", "flask",
        "mongodb", "sql server", "mysql", "postgresql",
        "aws", "azure", "gcp", "cloud", "docker", "kubernetes",
        "git", "github", "data structures", "algorithms", "oops"
    ],
    "Mechanical": [
        "autocad", "solidworks", "catia", "ansys", "creo",
        "thermodynamics", "fluid mechanics", "heat transfer",
        "cad", "cam", "cnc", "manufacturing", "hvac",
        "finite element analysis", "fea", "mechanical design",
        "quality control", "six sigma", "lean manufacturing",
        "gd&t", "machining", "welding", "robotics"
    ],
    "Civil": [
        "autocad", "staad pro", "revit", "structural analysis",
        "construction management", "surveying", "concrete design",
        "steel design", "geotechnical engineering", "estimation",
        "quantity surveying", "project management", "primavera",
        "building codes", "site supervision", "town planning",
        "hydraulics", "environmental engineering"
    ],
    "Electrical": [
        "circuit design", "power systems", "plc", "scada",
        "matlab", "simulink", "embedded systems", "microcontroller",
        "vlsi", "signal processing", "control systems",
        "power electronics", "renewable energy", "electrical design",
        "autocad electrical", "transformers", "switchgear"
    ]
}

def extract_skills(text, branch="IT/Computer Science"):
    text = text.lower()
    found_skills = []
    skill_list = SKILL_LISTS.get(branch, SKILL_LISTS["IT/Computer Science"])
    for skill in skill_list:
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text):
            found_skills.append(skill)
    return found_skills

def get_matching_keywords(resume, job_description, branch="IT/Computer Science"):
    resume_skills = set(extract_skills(resume, branch))
    jd_skills = set(extract_skills(job_description, branch))
    matched = resume_skills.intersection(jd_skills)
    missing = jd_skills - resume_skills
    return matched, missing

if __name__ == "__main__":
    sample_text = "I have experience in Python, SQL and React.js development"
    print(extract_skills(sample_text))