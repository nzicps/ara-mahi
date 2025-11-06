import requests
import psycopg2

API = "https://api.adzuna.com/v1/api/jobs/nz/search/1?app_id=7dc51f48&app_key=66c7e3acffa802c158d0a5de4f09e5b1&results_per_page=50&what=driver"

def fetch_nz_driver_jobs():
    print("Fetching NZ driver jobs...")
    r = requests.get(API)
    data = r.json()

    conn = psycopg2.connect(dbname="ara_mahi", user="postgres", host="localhost")
    cur = conn.cursor()

    for job in data.get("results", []):
        cur.execute("""
            INSERT INTO jobs (title, company, location, description, skills_required, url)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING;
        """, (
            job.get("title"),
            job.get("company", {}).get("display_name"),
            job.get("location", {}).get("area", ["Unknown"])[-1],
            job.get("description"),
            [],
            job.get("redirect_url")
        ))

    conn.commit()
    conn.close()
    print(" Jobs imported.")
    
if __name__ == "__main__":
    fetch_nz_driver_jobs()
