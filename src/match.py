import psycopg2, spacy

nlp = spacy.load("en_core_web_md")

def match():
    conn = psycopg2.connect(dbname="ara_mahi", user="postgres", host="localhost")
    cur = conn.cursor()

    cur.execute("SELECT name, location, skills FROM jobseekers ORDER BY id DESC LIMIT 1;")
    user = cur.fetchone()
    if not user:
        print("No jobseekers found.")
        return
    name, loc, skills = user
    seeker_vec = nlp(" ".join(skills))

    cur.execute("SELECT title, company, location, salary_min, salary_max, url FROM jobs;")
    jobs = cur.fetchall()

    scored = []
    for title, company, job_loc, smin, smax, url in jobs:
        job_vec = nlp(f"{title} {company} {job_loc}")
        scored.append((seeker_vec.similarity(job_vec), title, company, job_loc, smin, smax, url))

    scored.sort(reverse=True)
    print("\n🔥 TOP MATCHES:\n")
    for s, t, c, l, mn, mx, u in scored[:10]:
        print(f"{round(s,2)} | {t} @ {c} ({l}) ${mn}-{mx}\n → {u}\n")

if __name__ == "__main__":
    match()
