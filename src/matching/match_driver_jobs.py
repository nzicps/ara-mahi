import psycopg2

def match_driver_jobs():
    conn = psycopg2.connect(dbname="ara_mahi", user="postgres", host="localhost")
    cur = conn.cursor()

    print("\n=== Who do you want to match? ===")
    cur.execute("SELECT id, name, location FROM jobseekers ORDER BY id;")
    jobseekers = cur.fetchall()
    for js in jobseekers:
        print(f"{js[0]}) {js[1]} ({js[2]})")
    
    jobseeker_id = int(input("\nSelect jobseeker ID: "))

    cur.execute("SELECT name, location, skills FROM jobseekers WHERE id = %s;", (jobseeker_id,))
    name, location, skills = cur.fetchone()

    print(f"\nFinding **local driving jobs** near {location} for {name}...\n")

    driving_keywords = ['driver', 'class', 'truck', 'delivery', 'transport', 'forklift']

    query = """
        SELECT id, title, company, location, description, url
        FROM jobs
        WHERE (LOWER(title) LIKE ANY(%s) OR LOWER(description) LIKE ANY(%s))
          AND LOWER(location) LIKE LOWER(%s)
        ORDER BY id DESC
        LIMIT 20;
    """

    keyword_patterns = [f"%{k}%" for k in driving_keywords]
    location_match = f"%{location}%"

    cur.execute(query, (keyword_patterns, keyword_patterns, location_match))
    matches = cur.fetchall()

    if not matches:
        print(" No local driving jobs found yet. Try fetching more jobs:")
        print("python src/jobs/fetch_nz_driver_jobs.py")
    else:
        for job in matches:
            job_id, title, company, job_location, desc, url = job
            print(f" {title} @ {company} ({job_location})")
            print("  -", desc[:120], "...")
            print("  ", url, "\n")

    conn.close()

if __name__ == "__main__":
    match_driver_jobs()
