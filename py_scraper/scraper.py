#!/usr/bin/python3
"""
Uses BeautifulSoup4 and requests to parse Holberton School project pages.
Projects are presented to students via the school's intranet, and this
script is designed to allow you to log in and automatically create
the appropriate folder and all files necessary for the project.
"""
from bs4 import BeautifulSoup
from intranet import log_in
import re
import requests
import sys
import subprocess

class Project:
    """
    Contains project information.

    TODO: Split this up! Project should contain tasks which should have
    all of these attributes.
    """
    def __init__(self, task):
        self.name = get_name(task)
        self.fullname = get_fullname(task)
        self.directory = get_directories(task)
        self.number = get_project_number(task)
        self.prototype = get_prototype(task)
        self.task = task
        self.type = "python"

def check_git():
    """
    Function to see if the script is being ran from a git repository.

    Not currently used.
    """
    try:
        f = open('.git/config', 'r')
    except:
        print(".git/config not found. Start from your repo!")
        exit()
        if ("holbertonschool-higher_level_programming.git" not in f.read()):
            print("Incorrect git repo! Exiting.")
            exit()

def get_name(task):
    """
    Grabs the file name related to a task.

    TODO: We should be able to use BS4 for this...
    """
    flag = 0
    i = 0
    for string in task.strings:
        if (string == "File: "):
            flag = 1
        elif (flag == 1):
            return string.lstrip(' ')

def get_fullname(task):
    """
    Grabs the absolute path for a file related to a task.

    TODO: BS4
    """
    flag = 0
    i = 0
    for string in task.strings:
        if (string == "File: "):
            flag = 1
        elif (string == "Directory: "):
            flag = 2
        elif (flag == 1):
            fullname += string.lstrip()
            flag = 0
        elif (flag == 2):
            fullname = (string.lstrip() + "/")
            flag = 0
    return fullname

def get_prototype(task):
    """
    Grabs the prototype for a task, if avail.
    """
    flag = 0
    for string in task.strings:
        if (string == "Prototype: "):
            flag = 1
        elif (flag == 1):
            return string.lstrip(' ')

def print_fullname():
    """
    Prints all full file names for a project.
    """
    for project in plist:
         print(project.fullname)

def print_name():
    """
    Prints all non-absolute file names for a project.

    Shouldn't be necessary since we're building a list...
    """
    flag = 0
    for task in tasks:
        for string in task.strings:
            if (string == "File: "):
                flag = 1
            elif (flag == 1):
                print(string)
                flag = 0

def get_directories(task):
    """
    Grabs directories associated with a task
    """
    flag = 0
    for string in task.strings:
        if (string == "Directory: "):
            flag = 1
        elif (flag == 1):
            return string.lstrip(' ')
            flag = 0

def print_directories():
    """
    Prints all directories for a project.

    Shouldn't be necessary since we're building a list...
    """
    dirs = []
    for project in plist:
        if project.directory not in dirs:
            print (project.directory)
            dirs.append(project.directory)

def pythonsource(project):
    """
    Grabs raws for examples.

    Not really used...
    """
    for a in project.task.find_all("a", string="here"):
        newline = a["href"]
        newline = "https://raw.githubusercontent.com/" + newline[19:]
        start = newline.rfind('/blob/')
        newline = newline[:start] + newline[start + 5:]
        source = requests.get(newline)
        newfile = open(project.fullname, 'w')
        newfile.write(source.text)
        return (True)
    return (None)

def touch():
    """
    Script to run through all tasks in a project and touch associated files.
    """
    for project in plist:
        if (os.path.isdir(project.directory) != True):
            subprocess.call(["mkdir", project.directory])
        subprocess.call(["touch", project.fullname])
        template = get_template(project)
        if (template != None):
            file = open(project.fullname, "w")
            file.write(open(template, "r").read())
            if (project.prototype is not None):
                file.write(project.prototype + '\n')
        open(project.directory + "/README.md", "a").write(project.name + '\n')
        pythonsource(project)
        make_mains()

def get_template(project):
    """
    Finds templates for the scraper
    """
    if (re.search(".py$", project.name) != None):
        return("/usr/include/scraper/templates/python.template")
    if (re.search(".c$", project.name) != None):
        return("/usr/include/scraper/templates/c.template")
    if (re.search(".sh$", project.name) != None):
        return("/usr/include/scraper/templates/bash.template")
    return(None)

def print_all():
    """
    Prints all strings in the soup, shouldn't need this."
    """
    for string in soup.strings:
        print(string)

def error_soup():
    """
    Once again we don't need to do this this way.

    Can just check the status_code right?
    """
    if ("The page you were looking for doesn't exist (404)" in soup.strings):
        print("Incorrect project number, 404 error.")
        exit()
    if ("The project you requested is not available to you yet!" in soup.strings):
        print("Incorrect project number, not available.")
        exit()
    if ('{"success":false,"message":"You need to sign in before."}' in soup.strings):
        print("Incorrect login. Check that your cookies.txt is valid.")
        exit()

def usage_error():
    """
    Usage error info.
    """
    print("usage: {} projectnumber operation".format(sys.argv[0]))
    print("Possible operations: ")
    print("name - prints all filenames.")
    print("fullname - prints all filenames and the corresponding directory.")
    print("directories - gives a list of all directories used for the project.")
    print("touch - creates a folder (if needed) for each file, and creates a blank file for each.")
    print("all - prints the whole HTML result from the project page (prettified)")
    exit()

def get_extra():
    """
    Checks for extras
    """
    for task in tasks:
        print(get_extra(task))

def make_mains():
    """
    Creates main files
    """
    for task in tasks:
        for string in task.strings:
            result = re.search('cat(.)*main.py', string)
            if (result != None):
                filename = string[result.start(0) + 4:result.end(0)]
                if (filename != None):
                    direct = get_directories(task)
                    filename = direct + "/" + filename
                    user = re.search('(.)*@ubuntu:(.)*', string)
                    string = string[user.end(2) + 1:]
                    user = re.search('(.)*@ubuntu:(.)*', string)
                    string = string[:user.start(0)]
                    newfile = open(filename, 'w')
                    newfile.write(string)

def get_project_number(task):
    """
    Grabs task numbers
    """
    h4 = task.find('h4', class_="task")
    text = h4.text
    period = text.find('.')
    num = int(text[5:period])
    return (num)

def project_list():
    """
    Builds a list of projects.


    Should be tasks!
    """
    projectlist = [ Project(task) for task in tasks ]
    return projectlist


if __name__ == '__main__':
    if (len(sys.argv) < 3):
        usage_error()

    url = 'https://intranet.hbtn.io/projects/'
    url += sys.argv[1]

    session = requests.Session()
    if not log_in(session):
        exit()

    page = session.get(url)
    soup = BeautifulSoup(page.content, "lxml")
    tasks = soup.find_all('div', class_=" clearfix gap")

    plist = project_list()

    for project in plist:
        get_template(project)
    error_soup()
    if (sys.argv[2] == 'fullname'):
        print_fullname()
    elif (sys.argv[2] == 'name'):
        print_name()
    elif (sys.argv[2] == 'touch'):
        touch()
    elif (sys.argv[2] == 'directories'):
        print_directories()
    elif(sys.argv[2] == 'all'):
        print(soup.prettify())
    else:
        usage_error()


# TODO:
# Check for files before creating them
# Warn that file exists and is not empty and give option to overwrite?
# Append instead of write by default?
# Figure out best way to handle this.
