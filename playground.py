import sympy

# Simple sympy example
def sympy_hello_world():
  x = sympy.Symbol('x') 
  y = sympy.Symbol('y') 
  expr = sympy.Eq((x + 2) * (x-2) * (y +2), 0)
  print(f'hello world result {sympy.solve(expr)}')

# Using Sympy to solve two unknowns
def sympy_two_unknowns():
  x, y = sympy.symbols('x y')
  eq1 = sympy.Eq(x + y - 5)
  eq2 = sympy.Eq(x - y + 3)
  sol_dict = sympy.solve((eq1,eq2), (x, y))
  print(f'x = {sol_dict[x]}')
  print(f'y = {sol_dict[y]}')

def sympy_string_to_solved():
  raw_constraint = 'cell_width = canvas_width / 2'
  split_constraint = raw_constraint.split('=')
  right_side = sympy.sympify(split_constraint[1])
  print(right_side, '= 0', 'SOLUTION: ', sympy.solve(right_side)[0])

def sympy_set_x():
  x = sympy.symbols('x')
  expr = x + 1
  x = 2 # has no effect
  print(expr)

def sympy_set_x_working():
  x = sympy.symbols('x')
  x = 2 
  expr = x + 1
  print(expr)

def sympy_name_example():
  crazy = sympy.symbols('unrelated')
  print({crazy + 1})

def sym_no_symbols():
  canvas = {}
  canvas['width'] = 2
  expr = canvas['width'] + 1
  print(expr)

def sym_no_symbols_2():
  canvas = sympy.symbols('canvas')
  expr = sympy.sympify('canvas + 2')
  print(sympy.solve(expr, 0))

def prototype():
  canvas, width = sympy.symbols('canvas width')
  eq1 = sympy.Eq(canvas, 100)
  eq2 = sympy.Eq(width, canvas/2)
  print(sympy.solve((eq1, eq2), width))

if __name__ == "__main__":
  # sympy_hello_world()
  # sympy_string_to_solved()
  # sympy_set_x()
  # sympy_set_x_working()
  prototype()
