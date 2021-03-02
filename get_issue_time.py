import configparser
import json
import requests


config = configparser.ConfigParser()
config.read('config.ini')
conf = config["DEFAULT"]

USERNAME = "ali.veeve"
# conf["USER_NAME"]
PRIVATE_TOKEN = conf["PRIVATE_TOKEN"]
LABEL = "sprint::engr-may11"


class Time:

  def __init__(self, estimated_time):
    self.seconds = estimated_time
    self.hours = self.seconds/(60*60)

  def hours(self):
    return (self.seconds/(60*60))

  def seconds(self):
    return self.seconds


class Issue:

  def __init__(self, project_name, title, time, state):
    self.project = project_name
    self.title = title
    self.time = time
    self.state = state
    if state == "opened":
      self.is_open = True
    else:
      self.is_open = False

  def __str__(self):
    return (self.project + " " + " " + self.title + " " + " " + str(self.time))


class Sprint:

  def __init__(self):
    self.issues = []

  def add_issue(self, issue):
    self.issues.append(issue)

  def total_time(self):
    total_time = 0
    for issue in self.issues:
      if issue.is_open:
        total_time += issue.time
    return total_time

  def total_time_hours(self):
    return Time(self.total_time()).hours


if __name__ == "__main__":
  headers = {"PRIVATE-TOKEN":PRIVATE_TOKEN}
  r = requests.get(f"https://gitlab.com/api/v4/issues?assignee_username={USERNAME}&labels={LABEL}", headers=headers)
  issue_list = json.loads(r.text)

  this_sprint = Sprint();
  for issue in issue_list:
    project = issue["web_url"].split("/")[-4]
    state = issue["state"]
    new_issue = Issue(project, issue["title"], issue["time_stats"]["time_estimate"], state)
    this_sprint.add_issue(new_issue)

    if new_issue.is_open:
      print(new_issue.project, "|", new_issue.title, "|", Time(new_issue.time).hours)
      print(issue["web_url"])
      print("-----------------------------------------")

  total_time = this_sprint.total_time_hours()
  print(total_time)
