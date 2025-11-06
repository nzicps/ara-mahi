import psycopg2
import requests
from bs4 import BeautifulSoup

def save_job(title, company, location, url):
    conn = psycopg2.connect(dbname="ara_mahi", user="postgres", host="localhost")
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO jobs (title, company, location, url)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT DO NOTHING;
    """, (title, company, location, url))
    conn.commit()
    conn.close()

def load_seek_hamilton():
    print("?? Loading SEEK jobs...")
    url = "https://www.seek.co.nz/jobs/in-Hamilton-Waikato?page=1"
    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(r.text, "html.parser")

    for job in soup.select("article"):
        title_el = job.select_one("a[data-automation='jobTitle']")
        company_el = job.select_one("a[data-automation='jobCompany']")

        if not title_el:
            continue

        title = title_el.text.strip()
        company = company_el.text.strip() if company_el else "Unknown"
        save_job(title, company, "Hamilton", None)

def load_indeed_hamilton():
    print("?? Loading Indeed jobs...")
    url = "https://nz.indeed.com/jobs?q=&l=Hamilton%2C+Waikato"
    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(r.text, "html.parser")

    for card in soup.select(".result"):
        title_el = card.select_one("h2 a")
        company_el = card.select_one(".company")
        link = card.select_one("a")

        if not title_el:
            continue

        title = title_el.text.strip()
        company = company_el.text.strip() if company_el else "Unknown"
        job_url = "https://nz.indeed.com" + link["href"]
        save_job(title, company, "Hamilton", job_url)

if __name__ == "__main__":
    print("\n=== Loading NZ Jobs for Hamilton ===")
    load_seek_hamilton()
    load_indeed_hamilton()
    print("\n? Job Loading Complete!")
