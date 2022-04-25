from sympy import Interval, Symbol, S, sin, cos, pi, maximum

if __name__ == "__main__":
  x = Symbol('x')
  f = -x**2 + 2*x + 5
  maximum(f, x, S.Reals)
  maximum(sin(x), x, Interval(-pi, pi/4))
  maximum(sin(x)*cos(x), x)
  print(maximum(f, x, S.Reals))
