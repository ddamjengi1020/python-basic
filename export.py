import csv


def save_to_jobs(jobs):
    file = open("jobs.csv", mode="w")
    writer = csv.writer(file)
    writer.writerow(["title", "location", "company", "link"])
    for job in jobs:
      writer.writerow(list(job.values()))
    return
