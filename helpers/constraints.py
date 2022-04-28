import sympy
from enum import Enum

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

def parse_constraints(list_of_constraint_strings):
  parsed_constraints = []
  for constraint in list_of_constraint_strings:
    parsed_constraints.append(Constraint(constraint))
  return parsed_constraints

def strings_to_constraints(raw_string_list):
  results = []
  for raw_string in raw_string_list:
    constraint = string_to_constraint(raw_string)
    results.append(constraint)
  return results

def string_to_constraint(raw_string):
  processed_string = raw_string.replace('.', '_') # TODO - Improve
  return Constraint(processed_string)

if __name__ == "__main__":
  print('Test code here')
