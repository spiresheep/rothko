import json
from helpers.cell import Cell
from helpers.layout import Layout
from helpers.constraints import Constraint, strings_to_constraints

# Function that parses the layout configuration file and returns a Layout
def parse(file_name):
  number_of_unnamed = 0
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
    else:
      name = f'_cell{number_of_unnamed}'
      number_of_unnamed += 1
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
    for constraint in local['constraints']:
      raw_constraint_list.append(constraint)
  return Layout(cell_list, strings_to_constraints(raw_constraint_list))  
