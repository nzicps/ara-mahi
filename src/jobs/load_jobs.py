import psycopg2
import requests
from bs4 import BeautifulSoup

def save_job(title, company, location):
    conn = psycopg2.connect(dbname="ara_mahi", user="postgres", host="localhost")
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO jobs (title, company, location)
        VALUES (%s, %s, %s)
        ON CONFLICT DO NOTHING;
    """, (title, company, location))
    conn.commit()
    conn.close()

def load_seek_hamilton():
    url = "https://www.seek.co.nz/jobs/in-Hamilton-Waikato?page=1"
    print(f"Fetching jobs from: {url}")
    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(r.text, "html.parser")

    for job in soup.select("article"):
        title = job.select_one("a[data-automation='jobTitle']")
        company = job.select_one("a[data-automation='jobCompany']")

        if not title:
            continue

        title = title.text.strip()
        company = company.text.strip() if company else "Unknown"

        save_job(title, company, "Hamilton")

if __name__ == "__main__":
    print("\n=== Loading Hamilton Jobs from SEEK ===")
    load_seek_hamilton()
    print("? Done loading jobs.")
