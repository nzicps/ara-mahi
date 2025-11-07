from flask import Flask, jsonify, request
import psycopg2

app = Flask(__name__)

def db():
    return psycopg2.connect(dbname="ara_mahi", user="postgres", host="localhost")

@app.route("/")
def home():
    return "✅ Ara Mahi API is alive. Use /api/jobs, /api/match, /api/save, /api/saved/<phone>"

@app.route("/api/jobs")
def jobs():
    conn = db()
    cur = conn.cursor()
    cur.execute("SELECT title, company, location, salary_min, salary_max, url FROM jobs LIMIT 300;")
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
    if not user: return jsonify([])
    name, location, skills = user
    seeker_vec = nlp(" ".join(skills))
    cur.execute("SELECT title, company, location, salary_min, salary_max, url FROM jobs;")
    rows = cur.fetchall()
    conn.close()
    scored=[]
    for title, company, loc, mn, mx, url in rows:
        job_vec = nlp(f"{title} {company} {loc}")
        scored.append((seeker_vec.similarity(job_vec), title, company, loc, mn, mx, url))
    scored.sort(reverse=True)
    return jsonify([
        {"score": round(s,2), "title": t, "company": c, "location": l, "salary_min": mn, "salary_max": mx, "url": u}
        for s,t,c,l,mn,mx,u in scored[:25]
    ])

@app.route("/api/save", methods=["POST"])
def save_job():
    data = request.json
    user = data.get("phone")
    url = data.get("url")
    if not user or not url:
        return {"error": "missing"}, 400
    conn = db()
    cur = conn.cursor()
    cur.execute("INSERT INTO saved_jobs (user_phone, job_url) VALUES (%s,%s) ON CONFLICT DO NOTHING;", (user,url))
    conn.commit()
    conn.close()
    return {"status":"saved"}

@app.route("/api/saved/<phone>")
def saved(phone):
    conn = db()
    cur = conn.cursor()
    cur.execute("""
        SELECT j.title, j.company, j.location, j.salary_min, j.salary_max, j.url
        FROM saved_jobs s
        JOIN jobs j ON s.job_url = j.url
        WHERE s.user_phone = %s
        ORDER BY s.saved_at DESC;
    """, (phone,))
    rows = cur.fetchall()
    conn.close()
    return jsonify([
        {"title": t, "company": c, "location": l, "salary_min": mn, "salary_max": mx, "url": u}
        for t,c,l,mn,mx,u in rows
    ])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)
