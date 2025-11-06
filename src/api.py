from flask import Flask, jsonify
import psycopg2

app = Flask(__name__)

def db():
    return psycopg2.connect(dbname="ara_mahi", user="postgres", host="localhost")

@app.route("/")
def home():
    return "✅ Ara Mahi API is alive. Use /api/jobs or /api/match"
    
@app.route("/api/jobs")
def jobs():
    conn = db()
    cur = conn.cursor()
    cur.execute("SELECT title, company, location, salary_min, salary_max, url FROM jobs LIMIT 200;")
    rows = cur.fetchall()
    conn.close()
    return jsonify([
        {"title": t, "company": c, "location": l, "salary_min": mn, "salary_max": mx, "url": u}
        for t,c,l,mn,mx,u in rows
    ])

@app.route("/api/match")
def match():
    import spacy
    nlp = spacy.load("en_core_web_md")
    conn = db()
    cur = conn.cursor()

    cur.execute("SELECT name, location, skills FROM jobseekers ORDER BY id DESC LIMIT 1;")
    user = cur.fetchone()
    if not user:
        return jsonify([])

    name, location, skills = user
    seeker_vec = nlp(" ".join(skills))

    cur.execute("SELECT title, company, location, salary_min, salary_max, url FROM jobs;")
    jobs = cur.fetchall()
    conn.close()

    scored = []
    for title, company, job_loc, mn, mx, url in jobs:
        job_vec = nlp(f"{title} {company} {job_loc}")
        scored.append((seeker_vec.similarity(job_vec), title, company, job_loc, mn, mx, url))

    scored.sort(reverse=True)
    top = scored[:25]

    return jsonify([
        {"score": round(s,2), "title": t, "company": c, "location": l, "salary_min": mn, "salary_max": mx, "url": u}
        for s,t,c,l,mn,mx,u in top
    ])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)
