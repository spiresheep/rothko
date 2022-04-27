import sys
from helpers.cell import Cell
from helpers.dimensions import get_dimensions, MIN_WIDTH, MIN_HEIGHT, MAX_WIDTH, MAX_HEIGHT

SOURCE = {
  'WEST': 'west',
  'SOUTH':'south'
}

# Derived from Cell.
# Used to keep track of the neighboring nodes and current width of the cell.
class Node:
  def __init__(self, cell):
    self.cell = cell
    self._east = []
    self._width = cell.get_width()
    self._height = cell.get_height()

  # Returns a list of all the nodes touching the east side of the node
  def get_east(self):
    return self._east

  def append_east(self, node):
    self._east.append(node)

  def get_width(self):
    return float(self._width)

  def set_width(self, width):
    self._width = width

  def get_height(self):
    return float(self._height)

  def set_height(self, new_height):
    self._height = new_height

# Used to keep track of all the cells that make up a layout
class Graph:
  def __init__(self, cells):
    self.nodes = []
    for cell in cells:
      self.nodes.append(Node(cell))
    self.horizontal_source = Node(
      Cell(0, 0, 0, 'fixed', MAX_HEIGHT, 'fixed', 'WEST')
    )
    self.build_horizontal_graph(self.horizontal_source)
    # self.vertical_source = Node(
    #   Cell(0, 0, MAX_WIDTH, 'fixed', 0, 'fixed', 'SOUTH'))
    self._all_adaptable_cells = None #This is None for lazy execution

  def build_horizontal_graph(self, current_node):
    for other_node in self.nodes:
      if((current_node.cell.get_name() != other_node.cell.get_name()) &
          (current_node.cell.get_right() == other_node.cell.get_left())):
        current_node.append_east(other_node)
    if(current_node.get_east() == []):
      return
    else:
      for east in current_node.get_east():
        self.build_horizontal_graph(east)
      return

  def is_horizontal_1D(self):
    current_node = self.horizontal_source
    while(current_node.get_east() != []):
      if(len(current_node.get_east()) > 1):
        return False
      current_node = current_node.get_east()[0]
    return True

  # This is a function used for debugging
  def traverse_west_to_east(self):
    current_node = self.horizontal_source
    while(current_node != None):
      print(current_node.cell.get_name(), current_node.get_width())
      if(current_node.get_east() != []):
        current_node = current_node.get_east()[0]
      else:
        current_node = None

  # Get the horizontal source
  def get_horizontal_source(self):
    return self.horizontal_source

  def get_all_adaptable_cells(self):
    if(self._all_adaptable_cells == None):
      self._all_adaptable_cells = []
      current_node = self.get_horizontal_source()
      for current_node in self.nodes:
        if current_node.cell.w_policy == 'adaptable':
          self._all_adaptable_cells .append(current_node.cell)
    return self._all_adaptable_cells

  # Returns None if no such node exists
  def find_node(self, name):
    result = None
    for node in self.nodes:
      if(node.cell.get_name() == name):
        return node
    return result

  def set_node_width(self, name, width):
    node = self.find_node(name)
    node.set_width(width)

  def clone(self):
    return Graph(self.cells)

if __name__ == "__main__":
  print('Running tests for Graph.py')
  demo_cells = [
    Cell(0, 0, 100, 'adaptable', 100, 'adaptable', 'B'),
    Cell(0, 100, 100, 'adaptable', 100, 'adaptable', 'A'),
    Cell(0, 200, 100, 'adaptable', 100, 'adaptable', 'C'),
    Cell(0, 300, 100, 'adaptable', 100, 'adaptable', 'D')
  ]
  test_graph = Graph(demo_cells)
  print('Number of adaptable cells', len(test_graph.get_all_adaptable_cells()))
  test_graph.traverse_west_to_east()
