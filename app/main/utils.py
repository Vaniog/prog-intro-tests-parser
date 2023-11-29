import os
import git
import json
import requests
import webbrowser
import concurrent.futures
from bs4 import BeautifulSoup
from functools import partial
from app.config import Config


class NotFoundStudentException(Exception):
    def __init__(self, name, url):
        self.name = name
        self.url = url
        self.message = f"Error: Unable to find student {name} in a table in {url}"
        super().__init__(self.message)


def get_soup(url):
    response = requests.get(url)
    if response.status_code == 200:
        response.encoding = "utf-8"
        return BeautifulSoup(response.text, 'html.parser')
    else:
        raise Exception(f"Error: Unable to retrieve content from {url}. Status code: {response.status_code}")


# TODO remove name and group from table
def get_tablerow(url, name, osname):
    soup = get_soup(url)
    print(f"----Processing table for {osname}----")
    header = soup.find("tr")
    if header == None:
        raise Exception("Unknown exception, couldn't find rows in table")

    td = soup.find('td', string=name)
    if td == None or td.find_parent('tr') == None:
        raise NotFoundStudentException(name, url)

    return f"<table><tbody>{header}{td.find_parent('tr')}</tbody></table>"


def get_logtable(url, name, group, osname):
    soup = get_soup(url)
    print(f"----Processing logs for {osname}----")
    header = f"{name} ({group})"
    stripped_url = os.path.dirname(url) + "/"
    result = ""

    table_rows = soup.body.table.find_all("tr")

    i = 0
    th = None
    while th == None:
        if i >= len(table_rows):
            raise NotFoundStudentException(name, url)
        tr = table_rows[i]
        th = tr.find("th", string=header)
        i += 1

    th = None
    while th == None and i < len(table_rows):
        tr = table_rows[i]
        th = tr.find("th")
        if th == None:
            a = tr.find("a")
            if a != None:
                a["href"] = stripped_url + a["href"]
            result += str(tr)
        i += 1

    return f"<table><tbody>{result}</table></tbody>"


def gen_tables_for_os(os, name, group):
    html = ""
    table_url = f"https://www.kgeorgiy.info/upload/prog-intro/{os}/table.html"
    log_url = f"https://www.kgeorgiy.info/upload/prog-intro/{os}/logs.html"

    print(f"====Processing {os}====")
    html += f"<h1>{os}</h1>"

    with concurrent.futures.ThreadPoolExecutor() as executor:
        table_future = executor.submit(get_tablerow, table_url, name, os)
        log_future = executor.submit(get_logtable, log_url, name, group, os)
        table = table_future.result()
        log = log_future.result()

    html += "<h3>table</h3>"
    html += table

    html += "<h3>log</h3>"
    html += log

    return html


def gen_page(name, group):
    OSES = [
        "linux",
        "windows",
        "macos"
    ]

    html = ""
    with concurrent.futures.ThreadPoolExecutor() as executor:
        partial_function = partial(gen_tables_for_os, name=name, group=group)
        results = executor.map(partial_function, OSES)
        for result in results:
            html += result
    return html


def main(name):
    name_groups = dict()
    with open(os.path.join(Config.DATA_PATH, 'names.json'), encoding="UTF-8") as json_file:
        name_groups = json.load(json_file)
    if name not in name_groups:
        raise NotFoundStudentException("Wrong name")
    group = name_groups[name]
    html = gen_page(name, group)

    css = ""
    with open("output.css", "w", encoding="UTF-8") as css_file:
        css_file.write(css)

    return html


def get_names():
    with open(os.path.join(Config.DATA_PATH, 'names.json')) as json_file:
        return json.load(json_file)
