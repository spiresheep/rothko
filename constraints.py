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

def _proof_of_concept_constraints_from_cells_fixed(): #!!!!!!!!!!!!
  print('~~After Example~~')
  demo_cells = [
    Cell(0, 0, 100, 'fixed', 100, 'fixed', 'A'),
  ]
  layout = Layout(demo_cells)
  base_constraints = [f'MAX_WIDTH = {MAX_WIDTH}', f'MAX_WIDTH = {MIN_WIDTH}']
  

if __name__ == "__main__":
  print('~~Start Test~~')
  _proof_of_concept_parse_and_solve_single_fixed()
  _proof_of_concept_parse_and_solve_single_adaptable()
  print('~~End Test~~')
