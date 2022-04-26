from ast import Expression
from logging.handlers import SysLogHandler
from re import M
import sympy
from enum import Enum
from helpers.cell import Cell
from helpers.layout import Layout
from helpers.dimensions import MIN_WIDTH, MIN_HEIGHT, MAX_WIDTH, MAX_HEIGHT

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

# Below this is testing and scratch work

def _proof_of_concept_solve():
  canvas, width = sympy.symbols('canvas width')
  eq1 = sympy.Eq(canvas, 300)
  eq2 = sympy.Eq(width, canvas/2)
  print(sympy.solve((eq1, eq2), width))

def _how_to_calculate_max_min():
  # B is fixed, 
  canvas = sympy.symbols('canvas')
  eq2 = sympy.Poly(300 + (canvas * (MAX_WIDTH - canvas) - 300) - (canvas/2) + (canvas/2), canvas, domain=sympy.QQ)
  eq3 = (eq2, 0)
  END_POINTS = sympy.solve(eq3, canvas)
  for sol in END_POINTS:
    print('solution', sol, type(sol), abs(float(sol[0])))

def solve_min_max_fixed():
  print('~~~Current Test~~')
  x, function = sympy.symbols('x function')
  function = 300 + (x*0)
  print(function)
  min = sympy.minimum(function, x, sympy.Interval(MIN_WIDTH, MAX_WIDTH))
  max = sympy.maximum(function, x, sympy.Interval(MIN_WIDTH, MAX_WIDTH))
  print('Min', min, 'Max', max)

def solve_min_max_adaptable():
  print('~~~Current Test~~')
  x, function = sympy.symbols('x function')
  function =  (x) * (100 - x)
  print(function)
  min = sympy.minimum(function, x, sympy.Interval(MIN_WIDTH, MAX_WIDTH))
  max = sympy.maximum(function, x, sympy.Interval(MIN_WIDTH, MAX_WIDTH))
  print('Min', min, 'Max', max)

# Sympy claims'multivariate polynomials are not supported'
def _solve_min_max_adaptable():
  print('~~~Current Test~~')
  x = sympy.symbols('x')
  function = (x)*(MAX_WIDTH-x)
  print(function)
  min = sympy.minimum(function, x, sympy.Interval(MIN_WIDTH, MAX_WIDTH))
  max = sympy.maximum(function, x, sympy.Interval(MIN_WIDTH, MAX_WIDTH))
  print('Min', min, 'Max', max)

def coworker_hint():
  a, b, c, d, e, f, w = sympy.symbols('a, b, c, d, e, f, w')
  eq1 = sympy.Equality(a, b * 2)
  eq2 = sympy.Equality(e, a + c)
  eq3 = sympy.Equality(b, 100) #fixed
  eq4 = sympy.Equality(d, 200) #fixed
  eq5 = sympy.Equality(w, a + b + c + d + e + f)
  eq6 = sympy.Equality(w, 10000)
  #interate over all the undefined ones and make them equal each other!
  eq7 = sympy.Equality(c, f)
  print(sympy.solve((eq1, eq2, eq3, eq4, eq5, eq6, eq7), (a, b, c, d, e, f, w)))

def get_min_and_max():
  a, b, c, d, e, f, w = sympy.symbols('a, b, c, d, e, f, w')
  eq1 = sympy.Equality(a, b * 2)
  eq2 = sympy.Equality(e, a + c)
  eq3 = sympy.Equality(b, 100) #fixed
  eq4 = sympy.Equality(d, 200) #fixed
  eq5 = sympy.Equality(w, a + b + c + d + e + f)
  eq6 = sympy.Equality(c, f)
  # Minimize the leftovers to get min!
  eq7 = sympy.Equality(c, 0)
  print('The layout min is...' , sympy.solve((eq1, eq2, eq3, eq4, eq5, eq6, eq7), (a, b, c, d, e, f, w))[w])
  # Now to get max!? This doesn't seem right....
  eq7 = sympy.Equality(c, MAX_HEIGHT - a - b - d - e - f)
  print('The layout max is...' , sympy.solve((eq1, eq2, eq3, eq4, eq5, eq6, eq7), (a, b, c, d, e, f, w))[w])

def get_min_and_max_2():
  a, b, c, d, e, f, g, w = sympy.symbols('a, b, c, d, e, f, g, w')
  eq1 = sympy.Equality(a, b * 2)
  eq2 = sympy.Equality(e, a + c)
  eq3 = sympy.Equality(b, 100) #fixed
  eq4 = sympy.Equality(d, 200) #fixed
  eq5 = sympy.Equality(w, a + b + c + d + e + f + g)
  eq6 = sympy.Equality(c, f)
  eq8 = sympy.Equality(f, g)
  # Minimize the leftovers to get min!
  eq7 = sympy.Equality(c, 0)
  print('The layout min is...' , sympy.solve((eq1, eq2, eq3, eq4, eq5, eq6, eq7, eq8), (a, b, c, d, e, f,g, w))[w])
  # Now to get max!?
  eq7 = sympy.Equality(c, MAX_HEIGHT - a - b - d - e - f - g)
  print('The layout max is...' , sympy.solve((eq1, eq2, eq3, eq4, eq5, eq6, eq7, eq8), (a, b, c, d, e, f,g, w))[w])

def _proof_of_concept_2_parse_and_solve():
  c_1 = 'canvas_width = 0'
  c_2 = 'B_width = 50'
  c_3 = 'A_width = A_width'
  c_4 = 'canvas_width = A_width + B_width'
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

def _proof_of_concept_3_constraints_from_cells(): #!!!!!!!!!!!!
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
  coworker_hint()
  get_min_and_max()
  get_min_and_max_2()
  _proof_of_concept_2_parse_and_solve()
