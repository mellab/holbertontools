#!/usr/bin/python3
from bs4 import BeautifulSoup
import getpass
import http
import os
import requests


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
