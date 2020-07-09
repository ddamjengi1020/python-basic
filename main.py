from flask import Flask, render_template, request, redirect, send_file
from scrapper import get_jobs
from export import save_to_jobs
import os

app = Flask("whatever")

db = {}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/report")
def report():
    word = request.args.get("word")
    if word:
        word = word.lower()
        from_db = db.get(word)
        if from_db:
            jobs = from_db
        else:
            jobs = get_jobs(word)
            db[word] = jobs
    else:
        return redirect("/")
    return render_template(
        "report.html", searchingBy=word, resultsCount=len(jobs), jobs=jobs)


@app.route("/export")
def export():
    if os.path.exists("jobs.csv"):
      os.remove("jobs.csv")
    try:
        word = request.args.get("word")
        if not word:
            raise Exception()
        word = word.lower()
        jobs = db.get(word)
        if not jobs:
            raise Exception()
        save_to_jobs(jobs)
        if os.path.exists("jobs.csv"):
          return redirect("/jobs")
        else:
          raise Exception()
    except:
        return redirect("/")

@app.route("/jobs")
def download():
  return send_file("jobs.csv")

app.run(host="0.0.0.0")
