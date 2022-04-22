from ast import Expression
import sympy
from enum import Enum
from helpers.cell import Cell
from helpers.layout import Layout

class ConstraintClassification(Enum):
  BASE = 0 # A constrain that is 'solved' and used to solve other constraints
  EXPRESSION = 1 # A expression that needs to be solved

class ConstraintStatus(Enum):
  SOLVED = 0
  UNKNOWN = 1

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

def _proof_of_concept():
  canvas, width = sympy.symbols('canvas width')
  eq1 = sympy.Eq(canvas, 300)
  eq2 = sympy.Eq(width, canvas/2)
  print(sympy.solve((eq1, eq2), (width, canvas)))

if __name__ == "__main__":
  print('~~Start Test~~')
  x = sympy.symbols('x')
  x = 2 
  expr = x + 1
  print(expr)
  _proof_of_concept()
  print('~~After Example~~')
  demo_cells = [
    Cell(0, 0, 100, 'constrained', 100, 'fixed', 'A'),
    Cell(0, 100, 50, 'fixed', 50, 'fixed', 'B')
  ]
  layout = Layout(demo_cells)
  c_1 = 'canvas_width = 300'
  c_2 = 'A_width = canvas_width / 2'
  constraint_list = [c_1, c_2]
  parsed_constraints = []
  for constraint in constraint_list:
    parsed_constraints.append(Constraint(constraint))
  solution1 = sympy.solve((parsed_constraints[0].get_equation(), parsed_constraints[1].get_equation()), parsed_constraints[0].get_symbol())
  print('solution1', solution1)
  solution2 = sympy.solve((parsed_constraints[0].get_equation(), parsed_constraints[1].get_equation()), (parsed_constraints[0].get_symbol(), parsed_constraints[1].get_symbol()))
  print('solution2', solution2)

  #find cells, assign width!


