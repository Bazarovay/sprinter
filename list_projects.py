import configparser
import json
import requests
from requests.utils import quote

config = configparser.ConfigParser()
config.read('config.ini')
conf = config["DEFAULT"]

USERNAME = conf["USER_NAME"]
PRIVATE_TOKEN = conf["PRIVATE_TOKEN"]
HEADERS = {"PRIVATE-TOKEN": PRIVATE_TOKEN}

PROJECT_API_URL = "https://gitlab.com/api/v4/projects"
ORG_NAMESPACE = "my-smart-cart/veevesd"

def get_all_projects():
  r = requests.get(f"https://gitlab.com/api/v4/projects?membership=true&per_page=100", headers=HEADERS)
  return json.loads(r.text)


projects = get_all_projects()

for p in projects:
  print(p["ssh_url_to_repo"])