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
      r = requests.put(f"{self.api_url}/issues/{issue_iid}?labels={updated_labels}", headers=headers)
