import sympy
from helpers.dimensions import MIN_WIDTH, MAX_WIDTH

# Below this is testing and scratch work
def _proof_of_concept_solve():
  canvas, width = sympy.symbols('canvas width')
  eq1 = sympy.Eq(canvas, 300)
  eq2 = sympy.Eq(width, canvas/2)
  print(sympy.solve((eq1, eq2), width))

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

def shaobin_layout():
  a, b, c, d, e, f, w = sympy.symbols('a, b, c, d, e, f, w')
  eq1 = sympy.Equality(a, b * 2)
  eq2 = sympy.Equality(e, a + c)
  eq3 = sympy.Equality(b, 100) #fixed
  eq4 = sympy.Equality(d, 200) #fixed
  eq5 = sympy.Equality(w, a + b + c + d + e + f)
  eq6 = sympy.Equality(w, 1000)
  #interate over all the undefined ones and make them equal each other!
  eq7 = sympy.Equality(c, f)
  print('Shaobin', sympy.solve((eq1, eq2, eq3, eq4, eq5, eq6, eq7), (a, b, c, d, e, f, w)))

def get_min_and_max():
  a, b, c, d, e, f, w = sympy.symbols('a, b, c, d, e, f, w')
  eq1 = sympy.Equality(a, b * 2)
  eq2 = sympy.Equality(e, a + c)
  eq3 = sympy.Equality(b, 100) #fixed
  eq4 = sympy.Equality(d, 200) #fixed
  eq5 = sympy.Equality(w, a + b + c + d + e + f)
  eq6 = sympy.Equality(f, c + 10)
  # Minimize the leftovers to get min!
  eq7 = sympy.Equality(c, 0)
  print('The layout min is...' , sympy.solve((eq1, eq2, eq3, eq4, eq5, eq6, eq7), (a, b, c, d, e, f, w))[w])
  # Now to get max!? This doesn't seem right....
  eq7 = sympy.Equality(c, MAX_WIDTH - a - b - d - e - f)
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
  eq7 = sympy.Equality(c, MAX_WIDTH - a - b - d - e - f - g)
  print('The layout max is...' , sympy.solve((eq1, eq2, eq3, eq4, eq5, eq6, eq7, eq8), (a, b, c, d, e, f,g, w))[w])

def get_min_and_max_3(): # No regular blue!
  a, b, d, e, w = sympy.symbols('a, b, d, e, w')
  eq1 = sympy.Equality(a, b * 2)
  eq2 = sympy.Equality(e, w / 2)
  eq3 = sympy.Equality(b, 100) #fixed
  eq4 = sympy.Equality(d, 200) #fixed
  eq5 = sympy.Equality(w, a + e + b + d )
  # Minimize the leftovers to get min!
  print('The layout min is...' , sympy.solve((eq1, eq2, eq3, eq4, eq5), (a, b, d, e, w)))
  # Now to get max!?
  print('The layout max is...' , sympy.solve((eq1, eq2, eq3, eq4, eq5), (a, b, d, e, w)))

def get_mixed_policy(): # No regular blue!
  a, b, d, e, w, big = sympy.symbols('a, b, d, e, w, big')
  eq1 = sympy.Equality(a, b * 2)
  eq2 = sympy.Equality(e, w / 2)
  eq3 = sympy.Equality(b, 100) #fixed
  eq4 = sympy.Equality(d, 200) #fixed
  eq5 = sympy.Equality(w, a + e + b + d)
  eq7 = sympy.Equality(big, 300)
  # Minimize the leftovers to get min!
  print('The layout min is...' , sympy.solve((eq1, eq2, eq3, eq4, eq5, eq7), (a, b, d, e, w, big)))
  # Now to get max!?
  print('The layout max is...' , sympy.solve((eq1, eq2, eq3, eq4, eq5, eq7), (a, b, d, e, w, big)))

def proof_of_concept():
  a, b, c, d, w = sympy.symbols('a, b, c, d, w')
  eq1 = sympy.Equality(a, 100)
  eq2 = sympy.Equality(b,100)
  eq5 = sympy.Equality(w, a + b + c + d)
  width = sympy.Equality(w, 1000)
  adapt1 = sympy.Equality(c, w - a -b -d)
  adapt2 = sympy.Equality(d, w - a - b -c)
  print('The solution is...' , sympy.solve((eq1, eq2, eq5), (a, b, c, d, w)))

def rsplit_demo():
  thing = '_cell_width = 0'
  new_thing = thing.rsplit('_',1)
  print(new_thing, thing.count('_'))
  thing = 'C_height'
  new_thing = thing.rsplit('_',1)[1]
  print(new_thing)

if __name__ == "__main__":
  print('~~Start Test~~')
  # _proof_of_concept_solve()
  # shaobin_layout()
  # get_min_and_max()
  # get_min_and_max_2()
  # get_min_and_max_3()
  proof_of_concept()
  rsplit_demo()
