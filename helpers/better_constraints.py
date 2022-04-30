import sympy
from enum import Enum

class ConstraintClassification(Enum):
  LITERAL = 0 # A constrain that is 'solved' and used to solve other constraints
  EXPRESSION = 1 # A expression that needs to be solved

class Constraint:
  def __init__(self, constraint_string):
    self._constraint = constraint_string
    self.left = ''
    self.right = ''
    


class ConstraintSystem:
  def __init__(self):
    self._constraints = []
    self._symbolCollection = set()

  def __init__(self, fixed_strings):
    self._constraints = []
    self._symbolCollection = set()

  def add_constraint(constraint_str):
    parts = constraint_str.split('')
    for part in parts:
      

if __name__ == "__main__":
  print('Test code here')
