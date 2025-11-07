from flask import Flask, render_template, request, redirect
import requests

API = "https://ara-mahi-api.onrender.com"

app = Flask(__name__, template_folder="templates")

@app.route("/")
def home():
    jobs = requests.get(f"{API}/api/jobs").json()
    return render_template("jobs.html", jobs=jobs)

@app.route("/save", methods=["POST"])
def save():
    url = request.form["url"]
    phone = "test-user"
    requests.post(f"{API}/api/save", json={"phone":phone, "url":url})
    return redirect("/")

@app.route("/saved")
def saved():
    phone = "test-user"
    jobs = requests.get(f"{API}/api/saved/{phone}").json()
    return render_template("saved.html", jobs=jobs)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
