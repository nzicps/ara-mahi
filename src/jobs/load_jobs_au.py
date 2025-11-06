import psycopg2
import requests

APP_ID = "a2b2af58"
APP_KEY = "62adc59f50ca656023105803cb6e7a12"

def save_job(title, company, location, salary_min, salary_max, url):
    conn = psycopg2.connect(dbname="ara_mahi", user="postgres", host="localhost")
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO jobs (title, company, location, salary_min, salary_max, url)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT DO NOTHING;
    """, (title, company, location, salary_min, salary_max, url))
    conn.commit()
    conn.close()

def load_au_jobs():
    print("🌏 Loading Australia Jobs (Adzuna API)...")
    url = f"https://api.adzuna.com/v1/api/jobs/au/search/1?app_id={APP_ID}&app_key={APP_KEY}&results_per_page=50"

    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    data = r.json()

    results = data.get("results", [])
    for job in results:
        title = job.get("title", "Unknown")
        company = job.get("company", {}).get("display_name", "Unknown")
        location = job.get("location", {}).get("display_name", "Australia")
        salary_min = job.get("salary_min")
        salary_max = job.get("salary_max")
        url = job.get("redirect_url")

        save_job(title, company, location, salary_min, salary_max, url)

    print("✅ Done loading Australia jobs.")

if __name__ == "__main__":
    load_au_jobs()
