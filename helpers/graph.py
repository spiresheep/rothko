from helpers.cell import Cell

# Layout upper and lover bounds.
MIN_HEIGHT = 0
MAX_WIDTH = 2^24
MAX_HEIGHT = 2^24

SOURCE = {
  'WEST': 'west',
  'SOUTH':'south'
}

# Derived from Cell.
# Used to keep track of the neighbouting nodes and current width of the cell.
class Node:
  def __init__(self, cell):
    self.cell = cell
    self.east = []
    self.south = []

  def get_east(self):
    return self.east.copy()

  def set_east(self, new_east):
    self.east = new_east

  def get_south(self):
    return self.south.copy()

  def set_south(self, new_south):
    self.south = new_south

  south=property(get_south, set_south)
  east=property(get_east, set_east)

# Used to keep track of the relationships between Nodes (derived from cells)
class Graph:
  def __init__(self, cells):
    self.nodes = []
    for cell in cells:
      self.nodes.append(Node(cell))
    size = self.current_size()
    self.horizontal_source = Node(
      Cell(0, 0, 0, 'fixed', size['current_height'], 'fixed', 'WEST'))
    self.build_horizontal_graph(self.horizontal_source)
    self.vertical_source = Node(
      Cell(0, 0, 0, 'fixed', size['current_height'], 'fixed', 'SOUTH'))
    self.build_vertical_graph(self.vertical_source)

  def build_horizontal_graph(self, current_node):
    for node in self.nodes:
      if(current_node.get_right == node.get_left):
        current_node.east.append(node)
    if(node.east == []):
      return
    else:
      for east in self.current_node.get_east():
        self.build_horizontal_graph(east)
      return

  def build_vertical_graph(self, current_node):
    for node in self.nodes:
      if(current_node.get_bottom == node.get_top):
        current_node.south.append(node)
    if(node.south == []):
      return
    else:
      for south in self.current_node.get_south():
        self.build_horizontal_graph(south)
      return

  def is_horizontal_1D(self):
    current_node = self.horizontal_source
    while current_node.east != []:
      if(current_node.east > 1):
        return False
    return True

  def is_vertical_1D(self):
    current_node = self.vertical_source
    while current_node.south != []:
      if(current_node.south > 1):
        return False
    return True

  def is_horizontal_of_vertical(self):
    if self.is_horizontal_1D():
      return 'Horizontal'
    if self.is_horizontal_1D():
      return 'Vertical'
    return None