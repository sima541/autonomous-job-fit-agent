import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def clean_text(text):
    text = text.lower()                          # lowercase everything
    text = re.sub(r'[^a-z\s]', ' ', text)      # remove punctuation/special chars
    text = re.sub(r'\s+', ' ', text).strip()      # collapse extra whitespace
    return text

with open('../data/my_resume.txt', 'r') as f:
    resume_text = clean_text(f.read())

with open('job_description1.txt', 'r') as f:
    jd_text = clean_text(f.read())

print(resume_text[:300])
print(jd_text[:300])

# --- TF-IDF step ---
documents = [resume_text, jd_text]

vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = vectorizer.fit_transform(documents)

print(tfidf_matrix.shape)
print(vectorizer.get_feature_names_out()[:20])

similarity_score = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])
print("Match Score:", similarity_score[0][0])