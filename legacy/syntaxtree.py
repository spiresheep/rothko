class CASTNodeType(Enum):
  EQUATION = 0
  OPERATION = 1
  VARIABLE = 2
  EQUALS = 3
  NUMBER = 4

class OperationNode:
  def __init__(self):
    self.operation = ''

class VariableNode:
  def __init__(self):
    self.name = ''
    self.value = '' #unknown or none???

class EqualsNode:
  def __init__(self):
    self.left_side = ''
    self.right_side = ''

class NumberNode:
  def __init__(self):
    self.value = ''

class ConstraintAbstractSyntaxTree:
  def __init__(self, str):
    substrings = str.split(' ')

    print('Find the equals')
    print('split into left and right')
    print('Left is result')
    right = []
    while right != []:
      


class ConstraintAbstractSyntaxForest:
  def __init__(self, constraints):
    self._constraints = []
    for const in constraints:
      self._constraints.append(ConstraintAbstractSyntaxTree(const))

  def solve(inputs):
    