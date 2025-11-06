from flask import Flask, render_template
import psycopg2, os

app = Flask(__name__)

def db():
    return psycopg2.connect(
        dbname=os.environ.get("DB_NAME", "ara_mahi"),
        user=os.environ.get("DB_USER", "postgres"),
        password=os.environ.get("DB_PASSWORD", ""),
        host=os.environ.get("DB_HOST", "localhost"),
        port=os.environ.get("DB_PORT", "5432")
    )

@app.route("/")
def home():
    conn = db()
    cur = conn.cursor()
    cur.execute("SELECT title, company, location, salary_min, salary_max, url FROM jobs LIMIT 200;")
    jobs = cur.fetchall()
    conn.close()
    return render_template("jobs.html", jobs=jobs)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
