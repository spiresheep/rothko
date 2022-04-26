from asyncio import base_subprocess
from typing import final
import sympy
from enum import Enum
from helpers.cell import Cell
from helpers.layout import Layout
from helpers.dimensions import MIN_WIDTH, MAX_WIDTH

class ConstraintClassification(Enum):
  LITERAL = 0 # A constrain that is 'solved' and used to solve other constraints
  EXPRESSION = 1 # A expression that needs to be solved

class Constraint:
  def __init__(self, constraint):
    self._constraint = constraint
    self.parse_constraint()

  def parse_constraint(self):
    split = self._constraint.split('=')
    if(len(split) != 2):
      raise Exception('Constraint is badly formed')
    self._left = split[0]
    self._right = split[1]
    try:
      self._right = int(self._right)
      self._type = ConstraintClassification.LITERAL
    except ValueError:
      self._right = self._right
      self._type = ConstraintClassification.EXPRESSION
    self.symbol = sympy.sympify(self._left)

  def get_symbol(self):
    return self.symbol

  def get_equation(self):
    if(self._type == ConstraintClassification.LITERAL):
      return sympy.Eq(self.symbol, self._right)
    elif(self._type == ConstraintClassification.EXPRESSION):
      expression = sympy.sympify(self._right)
      return sympy.Eq(self.symbol, expression)

# Below this is testing
def _proof_of_concept_parse_and_solve_single_fixed():
  constraint_list = []
  constraint_list.append('B_width = 50')
  #constraint_list.append('A_width = A_width')
  constraint_list.append('canvas_width = B_width')
  parsed_constraints = []
  for constraint in constraint_list:
    parsed_constraints.append(Constraint(constraint))
  symbols_list = []
  f_list = []
  for constraint in parsed_constraints:
    symbols_list.append(constraint.get_symbol())
    f_list.append(constraint.get_equation())
  solution = sympy.solve(f_list, symbols_list) 
  print('solution for widths', solution)

def _proof_of_concept_parse_and_solve_single_adaptable():
  constraint_list = []
  constraint_list.append('canvas_width = A_width')
  # solve for min
  constraint_list.append('A = 0')
  parsed_constraints = []
  for constraint in constraint_list:
    parsed_constraints.append(Constraint(constraint))
  symbols_list = []
  f_list = []
  for constraint in parsed_constraints:
    symbols_list.append(constraint.get_symbol())
    f_list.append(constraint.get_equation())
  solution = sympy.solve(f_list, symbols_list) 
  print('min width', solution)
  # solve for min
  constraint_list = []
  constraint_list.append('canvas_width = A_width')
  constraint_list.append(f'MAX_WIDTH = {MAX_WIDTH}')
  constraint_list.append('A = MAX_WIDTH')
  parsed_constraints = []
  for constraint in constraint_list:
    parsed_constraints.append(Constraint(constraint))
  symbols_list = []
  f_list = []
  for constraint in parsed_constraints:
    symbols_list.append(constraint.get_symbol())
    f_list.append(constraint.get_equation())
  solution = sympy.solve(f_list, symbols_list)
  print('f_list', f_list)
  print('min width', solution)

def _proof_of_concept_constraints_from_cells_fixed():
  demo_cells = [
    Cell(0, 0, 100, 'fixed', 100, 'fixed', 'A'),
  ]
  layout = Layout(demo_cells)
  base_constraints = [f'MAX_WIDTH = {MAX_WIDTH}', f'MAX_WIDTH = {MIN_WIDTH}']
  fixed_constraints = []
  current_node = layout.graph.get_horizontal_source()
  while (current_node != None):
    if (current_node.cell.w_policy == 'fixed') & (current_node.cell.name != 'WEST'):
      fixed_constraints.append(f'{current_node.cell.name}_width = {current_node.cell.width}')
    if current_node.get_east() != []:
      current_node = current_node.get_east()[0]
    else:
      current_node = None
  full_constraint_list = base_constraints + fixed_constraints
  # Prase the constaints
  parsed_constraints = []
  for constraint in full_constraint_list:
    parsed_constraints.append(Constraint(constraint)) #!!!!
  # Create width_constraint 
  rhs = ''
  for constraint in parsed_constraints:
    if((str(constraint.get_symbol()) != 'MAX_WIDTH')  & (str(constraint.get_symbol()) != 'MIN_WIDTH')):
      if len(rhs) != 0:
        rhs = rhs + '+' + str(constraint.get_symbol())
      else:
        rhs = str(constraint.get_symbol())
  width_constraint = f'canavs_width = {rhs}'
  parsed_constraints.append(Constraint(width_constraint))
  #NOW SOLVE <3
  symbols_list = []
  f_list = []
  for constraint in parsed_constraints:
    symbols_list.append(constraint.get_symbol())
    f_list.append(constraint.get_equation())
  solution = sympy.solve(f_list, symbols_list)
  print('solution', solution)

def parse_constraints(list_of_constraint_strings):
  parsed_constraints = []
  for constraint in list_of_constraint_strings:
    parsed_constraints.append(Constraint(constraint))
  return parsed_constraints

def _proof_of_concept_constraints_from_cells_adaptable():
  demo_cells = [
    Cell(0, 0, 100, 'fixed', 100, 'fixed', 'B'),
    Cell(0, 100, 100, 'adaptable', 100, 'adaptable', 'A'),
  ]
  layout = Layout(demo_cells)


  fixed_constraints = []
  names_of_adaptable_cells = []
  current_node = layout.graph.get_horizontal_source()

  # Get constraints from fixed cells and adaptable cells
  while (current_node != None):
    print('current_node', current_node.cell.get_name())
    if (current_node.cell.w_policy == 'fixed') & (current_node.cell.name != 'WEST'):
      fixed_constraints.append(f'{current_node.cell.name}_width = {current_node.cell.width}')
    elif current_node.cell.w_policy == 'adaptable':
      names_of_adaptable_cells.append(current_node.cell.get_name())
    if (current_node.get_east() != []):
      current_node = current_node.get_east()[0]
    else:
      current_node = None
  # Generate the adaaptable cell constraint
  adaptable_constrains = []
  if(len(names_of_adaptable_cells) == 1):
    cell_name = names_of_adaptable_cells[0]
    adaptable_constrains.append(f'{cell_name}_width = {cell_name}_width ')
  elif(len(names_of_adaptable_cells) > 1):
    first_cell_name = names_of_adaptable_cells[0]
    for other_cell in names_of_adaptable_cells:
      adaptable_constrains.append(f'{first_cell_name}_width = {other_cell}_width')
    print(adaptable_constrains)

  #IF MIN_WIDTH OR MAX_WIDHTS ARE IN THE FORMULA... add plox
  base_constaints = []
  for constraint in fixed_constraints + adaptable_constrains:
    if 'MAX_WIDTH' in constraint:
      base_constaints = [f'MAX_WIDTH = {MAX_WIDTH}']
      break
  core_constraints = parse_constraints(base_constaints + fixed_constraints + adaptable_constrains)
  # Generate the canvas constraint
  rhs = ''
  for constraint in core_constraints:
    if((str(constraint.get_symbol()) != 'MAX_WIDTH')  & (str(constraint.get_symbol()) != 'MIN_WIDTH')):
      if len(rhs) != 0:
        rhs = rhs + '+' + str(constraint.get_symbol())
      else:
        rhs = str(constraint.get_symbol())
  width_constraint = f'canvas_width = {rhs}'
  core_constraints.append(Constraint(width_constraint))
  # Minimized adaptable cells
  minimizing_constraints = []
  if(len(names_of_adaptable_cells) == 1):
    cell_name = names_of_adaptable_cells[0]
    minimizing_constraints.append(f'{cell_name}_width = 0')
  #NOW SOLVE <3
  symbols_list = []
  f_list = []
  for constraint in core_constraints + parse_constraints(minimizing_constraints):
    symbols_list.append(constraint.get_symbol())
    f_list.append(constraint.get_equation())
  solution = sympy.solve(f_list, symbols_list)
  print('flist', f_list)
  print('symbols_list', symbols_list)
  print('Minimum Solution', solution)
  # Maximize adaptable cells
  maximzing_constraint = []
  if(len(names_of_adaptable_cells) >= 1):
    cell_name = names_of_adaptable_cells[0]
    print ('CELLLLL NAME', cell_name)
    current_node = layout.graph.get_horizontal_source()
    # Get constraints from fixed cells and adaptable cells
    rhs = ''
    while (current_node != None):
      if (current_node.cell.get_name() != cell_name) & (current_node.cell.get_name() != 'WEST'):
        name = current_node.cell.name + '_width'
        if len(rhs) != 0:
          rhs = rhs + '-' + name
        else:
          rhs = name
      if (current_node.get_east() != []):
        current_node = current_node.get_east()[0]
      else:
        current_node = None
    maximzing_constraint.append(f'{cell_name}_width = {MAX_WIDTH} - {rhs}')
    print('MAXIMIZING CONSTRAINT', maximzing_constraint)
  #NOW SOLVE <3
  symbols_list = []
  f_list = []
  for constraint in core_constraints + parse_constraints(maximzing_constraint):
    symbols_list.append(constraint.get_symbol())
    f_list.append(constraint.get_equation())
  #remove symbol duplicates
  solution = sympy.solve(f_list, symbols_list)
  print('flist', f_list)
  print('symbols_list', symbols_list)
  print('Maximum Solution', solution)

def _proof_of_concept_constraints_from_cells_MULTIPLE_adaptable():
  demo_cells = [
    Cell(0, 0, 100, 'fixed', 100, 'fixed', 'B'),
    Cell(0, 100, 100, 'adaptable', 100, 'adaptable', 'A'),
    Cell(0, 200, 100, 'adaptable', 100, 'adaptable', 'C')
  ]
  layout = Layout(demo_cells)


  fixed_constraints = []
  names_of_adaptable_cells = []
  current_node = layout.graph.get_horizontal_source()

  # Get constraints from fixed cells and adaptable cells
  while (current_node != None):
    #print('current_node', current_node.cell.get_name())
    if (current_node.cell.w_policy == 'fixed') & (current_node.cell.name != 'WEST'):
      fixed_constraints.append(f'{current_node.cell.name}_width = {current_node.cell.width}')
    elif current_node.cell.w_policy == 'adaptable':
      names_of_adaptable_cells.append(current_node.cell.get_name())
    if (current_node.get_east() != []):
      current_node = current_node.get_east()[0]
    else:
      current_node = None
  # Generate the adaaptable cell constraint
  adaptable_constrains = []
  if(len(names_of_adaptable_cells) == 1):
    cell_name = names_of_adaptable_cells[0]
    adaptable_constrains.append(f'{cell_name}_width = {cell_name}_width ')
  elif(len(names_of_adaptable_cells) > 1):
    first_cell_name = names_of_adaptable_cells[0]
    for other_cell in names_of_adaptable_cells:
      adaptable_constrains.append(f'{other_cell}_width = {first_cell_name}_width')
    
  print('ADAPTABLE CONSTRAINTS', adaptable_constrains)
  #IF MIN_WIDTH OR MAX_WIDHTS ARE IN THE FORMULA... add plox
  base_constaints = []
  for constraint in fixed_constraints + adaptable_constrains:
    if 'MAX_WIDTH' in constraint:
      base_constaints = [f'MAX_WIDTH = {MAX_WIDTH}']
      break
  core_constraints = parse_constraints(base_constaints + fixed_constraints + adaptable_constrains)
  # Generate the canvas constraint
  rhs = ''
  for constraint in core_constraints:
    if((str(constraint.get_symbol()) != 'MAX_WIDTH')  & (str(constraint.get_symbol()) != 'MIN_WIDTH')):
      if len(rhs) != 0:
        rhs = rhs + '+' + str(constraint.get_symbol())
      else:
        rhs = str(constraint.get_symbol())
  width_constraint = f'canvas_width = {rhs}'
  core_constraints.append(Constraint(width_constraint))
  # Minimized adaptable cells
  minimizing_constraint = []
  if(len(names_of_adaptable_cells) > 1):
    cell_name = names_of_adaptable_cells[0]
    minimizing_constraint.append(f'{cell_name}_width = 0')
  #NOW SOLVE <3
  symbols_list = []
  f_list = []
  for constraint in core_constraints + parse_constraints(minimizing_constraint):
    symbols_list.append(constraint.get_symbol())
    f_list.append(constraint.get_equation())
  solution = sympy.solve(f_list, symbols_list)
  print('flist', f_list)
  print('symbols_list', symbols_list)
  print('Minimum Solution', solution)
  # Maximize adaptable cells
  maximzing_constraint = []
  if(len(names_of_adaptable_cells) >= 1):
    cell_name = names_of_adaptable_cells[0]
    print ('CELLLLL NAME', cell_name)
    current_node = layout.graph.get_horizontal_source()
    # Get constraints from fixed cells and adaptable cells
    rhs = ''
    while (current_node != None):
      if (current_node.cell.get_name() != cell_name) & (current_node.cell.get_name() != 'WEST'):
        name = current_node.cell.name + '_width'
        if len(rhs) != 0:
          rhs = rhs + '-' + name
        else:
          rhs = name
      if (current_node.get_east() != []):
        current_node = current_node.get_east()[0]
      else:
        current_node = None
    maximzing_constraint.append(f'{cell_name}_width = {MAX_WIDTH} - {rhs}')
    print('MAXIMIZING CONSTRAINT', maximzing_constraint)
  #NOW SOLVE <3
  symbols_list = []
  f_list = []
  for constraint in core_constraints + parse_constraints(maximzing_constraint):
    symbols_list.append(constraint.get_symbol())
    f_list.append(constraint.get_equation())
  #remove symbol duplicates
  solution = sympy.solve(f_list, symbols_list)
  print('flist', f_list)
  print('symbols_list', symbols_list)
  print('Maximum Solution', solution)


def _proof_of_concept_constraints_from_cells_MULTIPLE_CELLS(): #!WIP
  demo_cells = [
    Cell(0, 0, 100, 'fixed', 100, 'fixed', 'B'),
    Cell(0, 100, 100, 'adaptable', 100, 'adaptable', 'A'),
    Cell(0, 200, 100, 'adaptable', 100, 'adaptable', 'C'),
    Cell(0, 300, 100, 'fixed', 100, 'fixed', 'D')
  ]
  layout = Layout(demo_cells)


  fixed_constraints = []
  names_of_adaptable_cells = []
  current_node = layout.graph.get_horizontal_source()

  # Get constraints from fixed cells and adaptable cells
  while (current_node != None):
    #print('current_node', current_node.cell.get_name())
    if (current_node.cell.w_policy == 'fixed') & (current_node.cell.name != 'WEST'):
      fixed_constraints.append(f'{current_node.cell.name}_width = {current_node.cell.width}')
    elif current_node.cell.w_policy == 'adaptable':
      names_of_adaptable_cells.append(current_node.cell.get_name())
    if (current_node.get_east() != []):
      current_node = current_node.get_east()[0]
    else:
      current_node = None
  # Generate the adaaptable cell constraint
  adaptable_constrains = []
  if(len(names_of_adaptable_cells) == 1):
    cell_name = names_of_adaptable_cells[0]
    adaptable_constrains.append(f'{cell_name}_width = {cell_name}_width ')
  elif(len(names_of_adaptable_cells) > 1):
    first_cell_name = names_of_adaptable_cells[0]
    for other_cell in names_of_adaptable_cells:
      adaptable_constrains.append(f'{other_cell}_width = {first_cell_name}_width')
    
  print('ADAPTABLE CONSTRAINTS', adaptable_constrains)
  #IF MIN_WIDTH OR MAX_WIDHTS ARE IN THE FORMULA... add plox
  base_constaints = []
  for constraint in fixed_constraints + adaptable_constrains:
    if 'MAX_WIDTH' in constraint:
      base_constaints = [f'MAX_WIDTH = {MAX_WIDTH}']
      break
  core_constraints = parse_constraints(base_constaints + fixed_constraints + adaptable_constrains)
  # Generate the canvas constraint
  rhs = ''
  for constraint in core_constraints:
    if((str(constraint.get_symbol()) != 'MAX_WIDTH')  & (str(constraint.get_symbol()) != 'MIN_WIDTH')):
      if len(rhs) != 0:
        rhs = rhs + '+' + str(constraint.get_symbol())
      else:
        rhs = str(constraint.get_symbol())
  width_constraint = f'canvas_width = {rhs}'
  core_constraints.append(Constraint(width_constraint))
  # Minimized adaptable cells
  minimizing_constraint = []
  if(len(names_of_adaptable_cells) > 1):
    cell_name = names_of_adaptable_cells[0]
    minimizing_constraint.append(f'{cell_name}_width = 0')
  #NOW SOLVE <3
  symbols_list = []
  f_list = []
  for constraint in core_constraints + parse_constraints(minimizing_constraint):
    symbols_list.append(constraint.get_symbol())
    f_list.append(constraint.get_equation())
  solution = sympy.solve(f_list, symbols_list)
  print('flist', f_list)
  print('symbols_list', symbols_list)
  print('Minimum Solution', solution)
  # Maximize adaptable cells
  maximzing_constraint = []
  if(len(names_of_adaptable_cells) >= 1):
    cell_name = names_of_adaptable_cells[0]
    print ('CELLLLL NAME', cell_name)
    current_node = layout.graph.get_horizontal_source()
    # Get constraints from fixed cells and adaptable cells
    rhs = ''
    while (current_node != None):
      if (current_node.cell.get_name() != cell_name) & (current_node.cell.get_name() != 'WEST'):
        name = current_node.cell.name + '_width'
        if len(rhs) != 0:
          rhs = rhs + '-' + name
        else:
          rhs = name
      if (current_node.get_east() != []):
        current_node = current_node.get_east()[0]
      else:
        current_node = None
    maximzing_constraint.append(f'{cell_name}_width = {MAX_WIDTH} - {rhs}')
    print('MAXIMIZING CONSTRAINT', maximzing_constraint)
  #NOW SOLVE <3
  symbols_list = []
  f_list = []
  for constraint in core_constraints + parse_constraints(maximzing_constraint):
    symbols_list.append(constraint.get_symbol())
    f_list.append(constraint.get_equation())
  #remove symbol duplicates
  solution = sympy.solve(f_list, symbols_list)
  print('flist', f_list)
  print('symbols_list', symbols_list)
  print('Maximum Solution', solution)


def _proof_of_concept_constraints_from_cells_WITH_CONSTRAINTS(): #!WIP
  demo_cells = [
    Cell(0, 0, 100, 'fixed', 100, 'fixed', 'B'),
    Cell(0, 100, 100, 'adaptable', 100, 'adaptable', 'A'),
    Cell(0, 200, 100, 'adaptable', 100, 'adaptable', 'C'),
    Cell(0, 300, 100, 'fixed', 100, 'fixed', 'D')
  ]
  layout = Layout(demo_cells)


  fixed_constraints = []
  names_of_adaptable_cells = []
  current_node = layout.graph.get_horizontal_source()

  # Get constraints from fixed cells and adaptable cells
  while (current_node != None):
    #print('current_node', current_node.cell.get_name())
    if (current_node.cell.w_policy == 'fixed') & (current_node.cell.name != 'WEST'):
      fixed_constraints.append(f'{current_node.cell.name}_width = {current_node.cell.width}')
    elif current_node.cell.w_policy == 'adaptable':
      names_of_adaptable_cells.append(current_node.cell.get_name())
    if (current_node.get_east() != []):
      current_node = current_node.get_east()[0]
    else:
      current_node = None
  # Generate the adaaptable cell constraint
  adaptable_constrains = []
  if(len(names_of_adaptable_cells) == 1):
    cell_name = names_of_adaptable_cells[0]
    adaptable_constrains.append(f'{cell_name}_width = {cell_name}_width ')
  elif(len(names_of_adaptable_cells) > 1):
    first_cell_name = names_of_adaptable_cells[0]
    for other_cell in names_of_adaptable_cells:
      adaptable_constrains.append(f'{other_cell}_width = {first_cell_name}_width')
    
  print('ADAPTABLE CONSTRAINTS', adaptable_constrains)
  #IF MIN_WIDTH OR MAX_WIDHTS ARE IN THE FORMULA... add plox
  base_constaints = []
  for constraint in fixed_constraints + adaptable_constrains:
    if 'MAX_WIDTH' in constraint:
      base_constaints = [f'MAX_WIDTH = {MAX_WIDTH}']
      break
  core_constraints = parse_constraints(base_constaints + fixed_constraints + adaptable_constrains)
  # Generate the canvas constraint
  rhs = ''
  for constraint in core_constraints:
    if((str(constraint.get_symbol()) != 'MAX_WIDTH')  & (str(constraint.get_symbol()) != 'MIN_WIDTH')):
      if len(rhs) != 0:
        rhs = rhs + '+' + str(constraint.get_symbol())
      else:
        rhs = str(constraint.get_symbol())
  width_constraint = f'canvas_width = {rhs}'
  core_constraints.append(Constraint(width_constraint))
  # Minimized adaptable cells
  minimizing_constraint = []
  if(len(names_of_adaptable_cells) > 1):
    cell_name = names_of_adaptable_cells[0]
    minimizing_constraint.append(f'{cell_name}_width = 0')
  #NOW SOLVE <3
  symbols_list = []
  f_list = []
  for constraint in core_constraints + parse_constraints(minimizing_constraint):
    symbols_list.append(constraint.get_symbol())
    f_list.append(constraint.get_equation())
  solution = sympy.solve(f_list, symbols_list)
  print('flist', f_list)
  print('symbols_list', symbols_list)
  print('Minimum Solution', solution)
  # Maximize adaptable cells
  maximzing_constraint = []
  if(len(names_of_adaptable_cells) >= 1):
    cell_name = names_of_adaptable_cells[0]
    print ('CELLLLL NAME', cell_name)
    current_node = layout.graph.get_horizontal_source()
    # Get constraints from fixed cells and adaptable cells
    rhs = ''
    while (current_node != None):
      if (current_node.cell.get_name() != cell_name) & (current_node.cell.get_name() != 'WEST'):
        name = current_node.cell.name + '_width'
        if len(rhs) != 0:
          rhs = rhs + '-' + name
        else:
          rhs = name
      if (current_node.get_east() != []):
        current_node = current_node.get_east()[0]
      else:
        current_node = None
    maximzing_constraint.append(f'{cell_name}_width = {MAX_WIDTH} - {rhs}')
    print('MAXIMIZING CONSTRAINT', maximzing_constraint)
  #NOW SOLVE <3
  symbols_list = []
  f_list = []
  for constraint in core_constraints + parse_constraints(maximzing_constraint):
    symbols_list.append(constraint.get_symbol())
    f_list.append(constraint.get_equation())
  #remove symbol duplicates
  solution = sympy.solve(f_list, symbols_list)
  print('flist', f_list)
  print('symbols_list', symbols_list)
  print('Maximum Solution', solution)



#END OF CURRENT WORK OF PROCESS
if __name__ == "__main__":
  print('~~Start Test~~')
  #_proof_of_concept_parse_and_solve_single_fixed()
  #_proof_of_concept_parse_and_solve_single_adaptable()
  #_proof_of_concept_constraints_from_cells_fixed()
  print('~~Adaptable Cell Demo~~')
  #_proof_of_concept_constraints_from_cells_adaptable()
  #_proof_of_concept_constraints_from_cells_MULTIPLE_adaptable()
  _proof_of_concept_constraints_from_cells_MULTIPLE_CELLS()
  print('~~End Test~~')
