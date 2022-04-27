import json
from helpers.cell import Cell

# Function that parses the layout configuration file and returns a list of cells.
def parse(file_name):
  file = open(file_name, 'r')
  pre_json = file.read()
  local = json.loads(pre_json)
  local = json.loads(pre_json)
  cells = []
  for cell in local['cells']:
    splitH = cell["horizontal"].split(" ")
    splitV = cell["vertical"].split(" ")
    name = ""
    if "name" in cell:
      name = cell["name"]
    newCell = Cell(
      cell["top"],
      cell["left"],
      float(splitH[0]),
      splitH[1],
      float(splitV[0]),
      splitV[1],
      name
    )
    cells.append(newCell)
  if('constraints' in local):
    print(local['constraints'])
    for constraint in local['constraints']:
      print(constraint)
  return cells
