import psycopg2, requests, time

APP_ID = "a2b2af58"
APP_KEY = "62adc59f50ca656023105803cb6e7a12"

def save_job(title, company, location, country, url, salary_min, salary_max):
    conn = psycopg2.connect(dbname="ara_mahi", user="postgres", host="localhost")
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO jobs (title, company, location, country, url, salary_min, salary_max)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT DO NOTHING;
    """, (title, company, location, country, url, salary_min, salary_max))
    conn.commit()
    conn.close()

def load_jobs(country_code):
    print(f"🌍 Loading jobs for {country_code.upper()}...")
    for page in range(1, 6):
        url = f"https://api.adzuna.com/v1/api/jobs/{country_code}/search/{page}?app_id={APP_ID}&app_key={APP_KEY}&results_per_page=50"
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        data = r.json()
        for job in data.get("results", []):
            save_job(job.get("title","Unknown"),
                     job.get("company",{}).get("display_name","Unknown"),
                     job.get("location",{}).get("display_name",""),
                     country_code.upper(),
                     job.get("redirect_url"),
                     job.get("salary_min"),
                     job.get("salary_max"))
        print(f"✅ Page {page} loaded")
        time.sleep(1)
    print(f"✅ Finished {country_code.upper()}")

if __name__ == "__main__":
    load_jobs("nz")
    load_jobs("au")
    print("🎉 All jobs imported.")
