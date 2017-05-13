#!/usr/bin/python3
from bs4 import BeautifulSoup
import getpass
import http
import os
import re
import requests
import sys

def log_in(session):
    """
    Python function for logging into the intranet.

    Needs to be passed a Requests session object so we can easily store the
    cookies, and further requests sent using this session will be authenticated
    as long as this succeeds.

    Returns True on success, Fail on failure.
    """

    url = 'https://intranet.hbtn.io/auth/sign_in'
    r = session.get(url)

    user = input("Enter your intranet login: ")
    pw = getpass.getpass("Enter your intranet password: ")

    if r.status_code != 200:
        print("Failed to fetch intranet page, check your network connection.")

    """
    Gotta grab the authentication token hidden in the HTML
    to send it as POST data. BS4 is the easiest way to do this.
    """
    soup = BeautifulSoup(r.text, 'html.parser')
    auth_token = soup.find('input', {'name': 'authenticity_token'})['value']

    data = {'user[login]': user,
            'user[password]': pw, 'user[remember_me]': 1,
            'commit': 'Log in', 'authenticity_token': auth_token}

    r = session.post(url, data=data)

    if r.url == url:
        print("Failed to log in. Check your login information and try again.")
        return False
    return True

def sort_tasks(soup):
    tasks = soup.find_all('div', class_=" clearfix gap")
    task_list = [Task(task) for task in tasks]

def parse_li_tags(task):
    for tag in task.find_all('li'):
        if "GitHub" in tag.contents[0]:
            repo = tag.contents[1].contents[0]
        if "File" in tag.contents[0]:
            filename = tag.contents[1].contents[0]
        if "Directory" in tag.contents[0]:
            directory = tag.contents[1].contents[0]
    try:
        return(repo, directory, filename)
    except:
        print("Errors parsing li tags to get GitHub repo, filename, directory.")
        print("Exiting out!")
        exit()

def parse_task_number(task):
    task_class = task.find('h4', class_="task")
    number = task_class.contents[0].strip().split(' ')[0]
    if number[-1] == '.':
        number = number[:-1]
    name = " ".join(task_class.contents[0].strip().split(' ')[1:])
    if "mandatory" in task_class.find('span').contents[0]:
        mandatory = True
    else:
        mandatory = False
    return(name, number, mandatory)

class Task:
    def __init__(self, task):
        self.id = task['id'][5:] # takes ex: task-875 and gives you 875
        self.name, self.number, self.mandatory = parse_task_number(task)
        self.repo, self.directory, self.filename = parse_li_tags(task)
        self.main = parse_main(task, self.number)
        print(self)

    def __repr__(self):
        desc = ["Task ID: {}".format(self.id),
                "Task number: {}".format(self.number),
                "Name: {}".format(self.name),
                "Is mandatory: {}".format(self.mandatory),
                "Repo: {}".format(self.repo),
                "Dir: {}".format(self.directory),
                "Filename: {}".format(self.filename),
                "Main file: \n{}".format(self.main)]
        return("\n".join(desc))


def parse_main(task, number):
    try:
        code = task.find('pre').find('code')
    except AttributeError: # triggers if there's no code blocks, thus no main
        return(None)
    if "cat {}-main".format(number) in code.contents[0]:
        string = code.contents[0]
        user = re.search('(.)*@ubuntu:(.)*', string)
        string = string[user.end(2) + 1:]
        user = re.search('(.)*@ubuntu:(.)*', string)
        string = string[:user.start(0)]
        return(string)
    return(None)




def parse_project(session, proj_number):
#    url = 'https://intranet.hbtn.io/projects/'
#    url += sys.argv[1]
#    page = session.get(url)
#    soup = BeautifulSoup(page.content, "lxml")
    with open('result.html', 'r') as fd:
        page = fd.read()
    soup = BeautifulSoup(page, "lxml")
    task_list = sort_tasks(soup)
    print("Project Description:")
    print(soup.find('article', class_="gap formatted-content"))

if __name__ == '__main__':
    session = requests.Session()
#    log_in(session)
#    proj_number = sys.argv[1]
    proj_number = 215
    parse_project(session, proj_number)
