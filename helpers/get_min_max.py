import numpy as np

MIN_X = 0
MIN_Y = 0
MAX_X = 2^24
MAX_Y = 2^24

def get_current_size(cells):
  max_width = 0
  max_height = 0
  for cell in cells:
    right = cell.get_right()
    bottom = cell.get_bottom()
    if right > max_width:
      max_width = right
    if bottom > max_height:
      max_height = bottom
  return {
    'current_width': max_width,
    'current_height': max_height
  }

def get_min_max(cells):
  col=[]
  for x in range(MAX_X+1):
    row=[]
    for y in range(MAX_Y+1):
      row.append(None)
    col.append(row)
  current_size=get_current_size(cells)
  width = current_size['current_width']
  height = current_size['current_height']
  col[width][height]=True
  explore(col, width, height)

def does_point_exist(width, height):
  if(MIN_X <= width & width <= MAX_X & MIN_Y <= height & height <= MAX_Y):
    return True
  return False

def explore(matrix, width, height):
  if(True):
    explore(matrix, width-1, height)
  if(True):
    explore(matrix, width, height-1)
  if(True):
    explore(matrix, width+1, height)
  if(True):
    explore(matrix, width, height+1)
  


def try_x_shrink(matrix, width, height):
  print('shrink x')
  if(True):
    return

def try_y_shrink():
  print('shrink x')
  if(True):
    return

def try_y_shrink():
  print('shrink x')
  if(True):
    return

def try_y_grow():
  print('shrink x')
  if(True):
    return