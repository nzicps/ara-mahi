from flask import Flask, render_template
import psycopg2

app = Flask(__name__)

def get_jobs():
    conn = psycopg2.connect(dbname="ara_mahi", user="postgres", host="localhost")
    cur = conn.cursor()
    cur.execute("SELECT title, company, location, salary_min, salary_max, url FROM jobs LIMIT 300;")
    data = cur.fetchall()
    conn.close()
    return data

@app.route("/")
def home():
    return render_template("jobs.html", jobs=get_jobs())

app.run(host="0.0.0.0", port=5000, debug=True)
