from flask import Flask, render_template, request, redirect
import requests

API = "https://ara-mahi-api.onrender.com"

app = Flask(__name__, template_folder="templates", static_folder="static")

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/set-phone", methods=["POST"])
def set_phone():
    phone = request.form["phone"]
    return redirect(f"/jobs?phone={phone}")

@app.route("/jobs")
def jobs():
    phone = request.args.get("phone")
    data = requests.get(f"{API}/api/jobs").json()
    return render_template("jobs.html", jobs=data, phone=phone)

@app.route("/save", methods=["POST"])
def save():
    phone = request.form["phone"]
    url = request.form["url"]
    requests.post(f"{API}/api/save", json={"phone":phone, "url":url})
    return redirect(f"/jobs?phone={phone}")

@app.route("/saved")
def saved():
    phone = request.args.get("phone")
    data = requests.get(f"{API}/api/saved/{phone}").json()
    return render_template("saved.html", jobs=data, phone=phone)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
