import configparser
import json
import requests
from requests.utils import quote
from jinja2 import Template
from csv2json import load_from_csv

config = configparser.ConfigParser()
config.read('config.ini')
conf = config["DEFAULT"]

USERNAME = conf["USER_NAME"]
PRIVATE_TOKEN = conf["PRIVATE_TOKEN"]
HEADERS = {"PRIVATE-TOKEN": PRIVATE_TOKEN}

PROJECT_API_URL = "https://gitlab.com/api/v4/projects"
ORG_NAMESPACE = "my-smart-cart/veevesd"

class Project:
  
  def __init__(self, project_name):
    """Initialize the project

    Arguments:
        project_name {[string]} -- namespace + project name: eg: veeveapps/picker-ui
    """
    self.project_id = project_name
    self.issues = []
    project_id = f"{ORG_NAMESPACE}/{self.project_id}"
    encoded_project_id = quote(project_id, safe='')
    self.api_url = f"{PROJECT_API_URL}/{encoded_project_id}"

  def get_open_issues(self):
    r = requests.get(f"{self.api_url}/issues?state=opened", headers=HEADERS)
    self.issues = json.loads(r.text)
    return self

  def add_labels_to_all(self, new_labels):
    for issue in self.issues:
      current_labels = issue["labels"]
      updated_labels = current_labels + new_labels
      issue_iid = issue["iid"]
      updated_labels = ",".join(updated_labels)
      print(issue["web_url"], issue_iid)
      print(updated_labels)
      r = requests.put(f"{self.api_url}/issues/{issue_iid}?labels={updated_labels}", headers=HEADERS)

  def create_issue(self, title, description, labels):
      updated_labels = ",".join(labels)
      print(updated_labels)
      request_str = f"{self.api_url}/issues/?title={title}&labels={updated_labels}&description={description}"
      r = requests.post(request_str, headers=HEADERS)
      return r

  def create_templated_issue(self, data):
      print(f"[create_templated_issue] Input:: data:{data}")
      response = self.create_issue(data["title"], get_issue_template(data), data["labels"])
      print(f"[create_templated_issue] Output:: response:{response}")

  def create_templated_issues(self, data):
      print(f"[create_template_issue] Input:: data:{data}")
      response_list = []
      for single_issue_data in data:
        response = self.create_templated_issue(single_issue_data)
        response_list.append(response)
      return response_list

def get_issue_template(data):
    f = open("issue.j2")
    templateContent = f.read()
    f.close()

    tm = Template(templateContent)
    msg = tm.render(data=data)
    return msg


def file_issues(keys, file_name):
  csv_file_path = file_name
  issues_data = load_from_csv(csv_file_path)

  project_name = "veevebackend/sps"
  sps = Project(project_name)
  response_list = sps.create_templated_issues(issues_data)
  print(response_list)


def cli(keys):
    intro = """
    Please add issue details
    """
    print(intro)
    issue_data = {}
    for key in keys:
      issue_data[key] = input(f"{key}:")

    issue_data["labels"] = issue_data["labels"].split(",")
    print(f"The data is f{issue_data}")

    project_name = "veevebackend/sps"
    sps = Project(project_name)

    response = sps.create_templated_issue(issue_data)
    print(response)

if __name__ == "__main__":
  path_str = """
  Please select one of the following input methods:
  1) file
  2) cli
  """
  print(path_str)
  option = input()

  if option not in ["1", "2"]:
    raise ValueError("Not a valid option")

  keys = ["title", "what", "why", "estimate", "acceptance_criteria", "labels"]

  if option == "1":
    file_name = "sprint_issues.csv"
    print("file upload")
    input("are you sure? File to upload " + file_name)
    file_issues(keys, file_name)
  elif option == "2":
    cli(keys)
