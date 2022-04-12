import json
from helpers.cell import Cell

# Function that parses the layout configuration file and returns a list of cells.
def parse(file_name):
  print('Start parse');
  file = open(file_name, 'r')
  pre_json = file.read()
  pre_json = '{"cells":[' + pre_json + ']}'
  pre_json = pre_json.replace('name:', '"name":')
  pre_json = pre_json.replace('horizontal:', '"horizontal":')
  pre_json = pre_json.replace('vertical:', '"vertical":')
  pre_json = pre_json.replace('top:', '"top":')
  pre_json = pre_json.replace('left:', '"left":')
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
      int(splitH[0]),
      splitH[1],
      int(splitV[0]),
      splitV[1],
      name
    )
    cells.append(newCell)
  print("Done parse")
  return cells
