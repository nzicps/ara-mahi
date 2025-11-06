# -*- coding: utf-8 -*-
import psycopg2
import requests

def save(title, company, location, url):
    conn = psycopg2.connect(dbname="ara_mahi", user="postgres", host="localhost")
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO jobs (title, company, location, url)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT DO NOTHING;
    """, (title, company, location, url))
    conn.commit()
    conn.close()

def load_trademe_hamilton():
    print("Loading TradeMe Hamilton jobs...")
    url = "https://api.trademe.co.nz/v1/Search/Jobs.json?region=14&district=72"
    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    data = r.json()

    for job in data.get("List", []):
        title = job.get("Title", "Unknown")
        company = job.get("Agency", "Unknown")
        listing_id = job.get("ListingId")
        job_url = f"https://www.trademe.co.nz/a/jobs/listing/{listing_id}.html" if listing_id else None
        save(title, company, "Hamilton", job_url)

if __name__ == "__main__":
    load_trademe_hamilton()
    print("Done.")
