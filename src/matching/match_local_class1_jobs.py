import psycopg2

def match_local_class1_jobs():
    conn = psycopg2.connect(dbname='ara_mahi', user='postgres', host='localhost')
    cur = conn.cursor()

    print("\n=== Select Jobseeker ===")
    cur.execute("SELECT id, name, location FROM jobseekers ORDER BY id;")
    for (jid, name, loc) in cur.fetchall():
        print(f"{jid}) {name} ({loc})")

    jobseeker_id = int(input("\nEnter jobseeker ID: "))

    cur.execute("SELECT name, location FROM jobseekers WHERE id = %s;", (jobseeker_id,))
    name, location = cur.fetchone()

    print(f"\nSearching **local Class 1-friendly jobs** for {name} in {location}...\n")

    query = """
        SELECT id, title, company, location, description, url
        FROM jobs
        WHERE
            (
                LOWER(title) LIKE ANY(%s)
                OR LOWER(description) LIKE ANY(%s)
            )
            AND LOWER(location) LIKE LOWER(%s)
            AND (
                title NOT ILIKE '%class 2%'
                AND title NOT ILIKE '%class 4%'
                AND title NOT ILIKE '%class 5%'
                AND description NOT ILIKE '%class 2%'
                AND description NOT ILIKE '%class 4%'
                AND description NOT ILIKE '%class 5%'
            )
        ORDER BY id DESC
        LIMIT 25;
    """

    keywords = ['driver', 'courier', 'delivery', 'van', 'warehouse', 'transport', 'logistics']
    patterns = [f"%{k}%" for k in keywords]
    location_match = f"%{location}%"

    cur.execute(query, (patterns, patterns, location_match))
    results = cur.fetchall()

    if not results:
        print(" No suitable local Class 1 jobs found yet. Try fetching more jobs: python src/jobs/fetch_nz_driver_jobs.py")
    else:
        for job in results:
            job_id, title, company, loc, desc, url = job
            print(f" {title} @ {company} ({loc})")
            print("   ", desc[:120], "...")
            print("   ", url, "\n")

    conn.close()

if __name__ == '__main__':
    match_local_class1_jobs()
