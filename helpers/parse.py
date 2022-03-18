from helpers.cell import Cell
import json

def parse(file_name):
  print('Start parse');
  file = open(file_name, 'r')
  local = json.loads(file.read())
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
