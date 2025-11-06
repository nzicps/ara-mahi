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

def load_indeed_hamilton():
    search_url = "https://nz.indeed.com/jobs?q=&l=Hamilton%2C+Waikato"
    print(f"Fetching: {search_url}")

    r = requests.get(search_url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(r.text, "html.parser")

    for card in soup.select(".result"):
        title_el = card.select_one("h2 a")
        company_el = card.select_one(".company")
        link = card.select_one("a")

        if not title_el:
            continue

        title = title_el.text.strip()
        company = company_el.text.strip() if company_el else "Unknown"
        url = "https://nz.indeed.com" + link["href"]
        save_job(title, company, "Hamilton", url)

if __name__ == "__main__":
    print("\n=== Loading Hamilton Jobs from Indeed ===")
    load_indeed_hamilton()
    print("? Done.")
