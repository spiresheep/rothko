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

# A layout contains all the data needed to display and modify a layout
class Layout:
  def __init__(self, cells):
    self.initial_cells = cells
    # These initial values are not the final values
    # The min and max values might be better defaults.
    bounds = get_dimensions(cells)
    canvas_width = bounds[0]
    canvas_height = bounds[1]
    self.min_width = canvas_width
    self.max_width = canvas_width
    self.min_height = canvas_height
    self.max_height = canvas_height
    # Generate some extra data about the layout - immutable properties - to cut
    # down on repetitive work. 
    self.horizontal = None
    self.vertical = None
    # Then build the graph
    self.graph = None

  def get_bounds(self):
    raise Exception('Not implimented')

  def resize_layout(self, new_width, new_height):
    raise Exception('Not implimented')
