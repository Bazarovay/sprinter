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