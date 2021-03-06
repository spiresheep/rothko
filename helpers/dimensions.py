# The lower bound on the canvas width
MIN_WIDTH = 0
# The lower bound on the canvas height
MIN_HEIGHT = 0
# The upper bound on the canvas width
MAX_WIDTH = 16777216
# The upper bound on the canvas height
MAX_HEIGHT = 16777216

# Determines the size of the canvas required to display the current list of cells
def get_dimensions(cells):
  max_width = 0
  max_height = 0
  for cell in cells:
    right = cell.get_right()
    bottom = cell.get_bottom()
    if right > max_width:
      max_width = right
    if bottom > max_height:
      max_height = bottom
  return {'width': max_width, 'height': max_height}

# Determines the size of the canvas required to display the current graph
def get_dimensions_from_graph(graph):
  width = 0
  height = 0
  current_node = graph.get_horizontal_source()
  while current_node != None:
    width = width + current_node.get_width()
    if(current_node.get_east() != []):
      current_node = current_node.get_east()[0]
    else:
      current_node = None
  current_node = graph.get_vertical_source()
  while current_node != None:  
    height = height + current_node.get_height()
    if(current_node.get_south() != []):
      current_node = current_node.get_south()[0]
    else:
      current_node = None
  return {'width': width, 'height': height}
