import ast
import sympy
from helpers.cell import Cell
from helpers.layout import Layout, LayoutClassification

# A class that is a hybrid between Cell and Node used to experiment with
class Cell_Node:
  def __init__(self, top, left, width, w_policy, height, h_policy, name):
    self._left = left
    self._top = top
    self._width = width
    self._height = height
    self._name = name
    self._w_policy = w_policy
    self._h_policy = h_policy

def solve_constraints(equations: list):
  print('TODO - SOMETHING')

def sympy_hello_world():
  x = sympy.Symbol('x') 
  y = sympy.Symbol('y') 
  expr = sympy.Eq((x + 2) * (x-2) * (y +2), 0)
  print(f'hello world result {sympy.solve(expr)}')

def sympy_two_unknowns():
  x, y = sympy.symbols('x y')
  eq1 = sympy.Eq(x + y - 5)
  eq2 = sympy.Eq(x - y + 3)
  sol_dict = sympy.solve((eq1,eq2), (x, y))
  print(f'x = {sol_dict[x]}')
  print(f'y = {sol_dict[y]}')

def sympy_string_to_solved():
  print('~ Start String demo ~')
  #cell_width, canvas_width = sympy.symbols('cell_width canvas_width')
  raw_constraint = 'cell_width = canvas_width / 2'
  split_constraint = raw_constraint.split('=')
  right_side = sympy.sympify(split_constraint[1])
  expression = sympy.sympify('canvas_width', 100)
  print('solution', right_side, type(right_side))
  print('~ End String demo ~')


def sympy_proof_of_concept():
  # cells = [
  #   Cell(0, 0, 100, 'adaptable', 100, 'fixed', 'A_Cell'),
  #   Cell(0, 100, 100, 'fixed', 100, 'fixed', 'B_Cell')
  # ]
  # layout = Layout(cells)
  # raw_constraint = 'A_Cell.width = Canvas.width / 2'
  # MAKE AST for each constraint/operation (???)
  raise Exception('Uh, you didn\'t implement anything')

if __name__ == "__main__":
  sympy_string_to_solved()