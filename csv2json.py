import csv, json

def is_an_array(value):
  return "#" in value

def load_from_csv(csv_file_path):
  data = []
  with open(csv_file_path) as csvFile:
    csvReader = csv.DictReader(csvFile)
    for rows in csvReader:
      row_json = {}
      print(rows)
      for key, value in rows.items():
        value = value.strip()
        if is_an_array(value):
          value = value.split("#")
        row_json[key.strip()] = value
      data.append(row_json)
  return data

if __name__ == "__main__":
  result = load_from_csv("sprint_issues.csv")
  print(result)