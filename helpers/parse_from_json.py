import json
from cell import Cell
from constraints import Constraint, strings_to_constraints

# Function that parses the layout configuration file and returns a list of cells.
def parse(file_name):
  file = open(file_name, 'r')
  pre_json = file.read()
  local = json.loads(pre_json)
  local = json.loads(pre_json)
  cell_list = []
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
    cell_list.append(newCell)
  raw_constraint_list = []
  if('constraints' in local):
    #print(local['constraints'])
    for constraint in local['constraints']:
      raw_constraint_list.append(constraint)
  #print('Done Parse')
  return {
    'cells': cell_list,
    'constraint': strings_to_constraints(raw_constraint_list)
  }
