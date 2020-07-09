import requests
from bs4 import BeautifulSoup

LIMIT = 50


def JOB_LINK(id):
    return f"http://www.saramin.co.kr/zf_user/jobs/relay/view?isMypage=no&rec_idx={id}"


def get_last_pages(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text, 'html.parser')
    pagination = soup.find("div", {"class": "pagination"})
    if pagination:
        links = pagination.find_all("a")
        pages = []
        if links:
            for link in links:
                pages.append(int(link["page"]))
            max_page = pages[-2]
        else:
            max_page = 1
    else:
        max_page = 0
    return max_page


def extract_job(html, id):
    title = html.find("h2", {"class": "job_tit"}).find("a")["title"]
    company = html.find("strong", {"class": "corp_name"}).find("a")["title"]
    job_link = JOB_LINK(id)
    loc_list = html.find("div", {"class": "job_condition"}).find_all("a")
    location = ""
    if len(loc_list) == 2:
        location = f"{loc_list[0].text + ' ' + loc_list[1].text}"
    else:
        location = f"{loc_list[0].text}"
    return {
        "title": title,
        "location": location,
        "company": company,
        "link": job_link
    }


def extract_jobs(last_page, url):
    jobs = []
    for page in range(last_page):
        result = requests.get(f"{url}&recruitPage={page+1}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "item_recruit"})
        if results:
            for result in results:
                job = extract_job(result, result["value"])
                jobs.append(job)
        print(f"Current scrapping page : {page + 1}")
    return jobs


def get_jobs(word):
    URL = f"http://www.saramin.co.kr/zf_user/search/recruit?searchword={word}&recruitPageCount={LIMIT}"
    last_page = get_last_pages(URL)
    if not last_page:
        jobs = []
    else:
        jobs = extract_jobs(last_page, URL)
    return jobs
