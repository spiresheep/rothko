from ast import Expression
from logging.handlers import SysLogHandler
import sympy
from enum import Enum
from helpers.cell import Cell
from helpers.layout import Layout

class ConstraintClassification(Enum):
  BASE = 0 # A constrain that is 'solved' and used to solve other constraints
  EXPRESSION = 1 # A expression that needs to be solved

# class ConstraintStatus(Enum):
#   SOLVED = 0
#   UNKNOWN = 1

class Constraint:
  def __init__(self, constraint):
    self._constraint = constraint
    self.get_classification()


  def get_classification(self):
    split = self._constraint.split('=')
    if(len(split) != 2):
      raise Exception('Constraint is badly formed')
    self._left = split[0]
    self._right = split[1]
    try:
      self._right = int(self._right)
      self._type = ConstraintClassification.BASE
    except ValueError:
      self._right = self._right
      self._type = ConstraintClassification.EXPRESSION
    self.symbol = sympy.sympify(self._left)

  def get_symbol(self):
    return self.symbol

  def get_equation(self):
    if(self._type == ConstraintClassification.BASE):
      return sympy.Eq(self.symbol, self._right)
    elif(self._type == ConstraintClassification.EXPRESSION):
      expression = sympy.sympify(self._right)
      return sympy.Eq(self.symbol, expression)

def _proof_of_concept_solve():
  canvas, width = sympy.symbols('canvas width')
  eq1 = sympy.Eq(canvas, 300)
  eq2 = sympy.Eq(width, canvas/2)
  print(sympy.solve((eq1, eq2), (width, canvas)))

def _proof_of_concept_2_parse_and_solve():
  c_1 = 'canvas_width = 300'
  c_2 = 'B_width = 50'
  c_3 = 'canvas_leftovers = canvas_width - B_width' #how to compose
  c_4 = 'A_width = canvas_leftovers / 1'
  constraint_list = [c_1, c_2, c_3, c_4]
  parsed_constraints = []
  for constraint in constraint_list:
    parsed_constraints.append(Constraint(constraint))
  #solve
  symbols_list = []
  f_list = []
  for constraint in parsed_constraints:
    symbols_list.append(constraint.get_symbol())
    f_list.append(constraint.get_equation())
  solution = sympy.solve(f_list, symbols_list) 
  print('solution for widths', solution)


def _proof_of_concept_3():
  c_1 = 'canvas_width = '
  c_2 = 'B_width = 50'
  c_3 = 'canvas_leftovers = canvas_width - B_width' #how to compose
  c_4 = 'A_width = canvas_leftovers / 1'
  constraint_list = [c_1, c_2, c_3, c_4]
  parsed_constraints = []
  for constraint in constraint_list:
    parsed_constraints.append(Constraint(constraint))
  #solve
  symbols_list = []
  f_list = []
  for constraint in parsed_constraints:
    symbols_list.append(constraint.get_symbol())
    f_list.append(constraint.get_equation())
  solution = sympy.solve(f_list, symbols_list) 
  print('solution for widths', solution)

def _proof_of_concept_2_solve_canvas_size():
  c_2 = 'B_width = 50'
  c_1 = 'canvas_width = B_width + A_width'
  c_3 = 'canvas_leftovers = canvas_width - B_width' #how to compose
  c_4 = 'A_width = canvas_leftovers / 1'
  c_4 = 'A_width = 200'
  constraint_list = [c_1, c_2, c_3, c_4]
  parsed_constraints = []
  for constraint in constraint_list:
    parsed_constraints.append(Constraint(constraint))
  #solve
  symbols_list = []
  f_list = []
  for constraint in parsed_constraints:
    symbols_list.append(constraint.get_symbol())
    f_list.append(constraint.get_equation())
  solution = sympy.solve(f_list, symbols_list) 
  print('solution for canvas', solution)

def _proof_of_concept_3_constraints_from_cells():
  print('~~After Example~~')
  demo_cells = [
    Cell(0, 0, 100, 'adaptable', 100, 'fixed', 'A'),
    Cell(0, 100, 50, 'fixed', 50, 'fixed', 'B')
  ]
  layout = Layout(demo_cells)
  c_1 = 'canvas_width = 300'
  c_2 = 'B_width = 50' #because B width is fixed
  c_3 = 'canvas_leftovers = canvas_width - Y'
  c_4 = 'A_width = canvas_leftovers / X'
  constraint_list = [c_1, c_2, c_3, c_4]
  parsed_constraints = []
  for constraint in constraint_list:
    parsed_constraints.append(Constraint(constraint))
  #solve
  symbols_list = []
  f_list = []
  for constraint in parsed_constraints:
    symbols_list.append(constraint.get_symbol())
    f_list.append(constraint.get_equation())
  solution = sympy.solve(f_list, symbols_list) 
  print('solution', solution)

if __name__ == "__main__":
  print('~~Start Test~~')
  x = sympy.symbols('x')
  x = 2 
  expr = x + 1
  print(expr)
  _proof_of_concept_2_parse_and_solve()
  _proof_of_concept_2_solve_canvas_size()


