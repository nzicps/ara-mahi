import psycopg2
import requests
import xml.etree.ElementTree as ET

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

def load_govt_jobs():
    print("Å® Loading from jobs.govt.nz...")
    url = "https://jobs.govt.nz/feed/feeds/health.xml"
    r = requests.get(url)
    root = ET.fromstring(r.content)

    for item in root.findall(".//item"):
        title = item.findtext("title") or "Unknown"
        company = item.findtext("author") or "Government"
        link = item.findtext("link")
        save_job(title, company, "New Zealand", link)

def load_trademe_hamilton():
    print("Å® Loading from TradeMe Jobs (Hamilton)...")
    url = "https://api.trademe.co.nz/v1/Search/Jobs.json?region=Waikato"
    r = requests.get(url)
    data = r.json()

    for job in data.get("List", []):
        title = job.get("Title", "Unknown")
        company = job.get("Company", "Unknown")
        link = job.get("ListingURL", "")
        save_job(title, company, "Waikato", link)

def load_linkedin_hamilton():
    print("Å® Loading from LinkedIn RSS (Hamilton)...")
    rss_url = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=&location=Hamilton%2C%20Waikato"
    r = requests.get(rss_url, headers={"User-Agent": "Mozilla/5.0"})
    # LinkedIn returns HTML fragments of job cards; we just extract text visually
    import re
    jobs = re.findall(r'title="([^"]+)"', r.text)
    for title in jobs:
        save_job(title, "LinkedIn", "Hamilton", "https://linkedin.com/jobs")

if __name__ == "__main__":
    load_govt_jobs()
    load_trademe_hamilton()
    load_linkedin_hamilton()
    print("? Done loading real jobs.")
