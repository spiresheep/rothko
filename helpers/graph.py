from helpers.cell import Cell
from helpers.dimensions import MAX_WIDTH, MAX_HEIGHT

SOURCE = {
  'WEST': 'west',
  'NORTH':'north'
}

# Used to keep track of the neighboring nodes and current width of the cell.
class Node:
  def __init__(self, cell):
    self.cell = cell
    self._east = []
    self._south = []
    self._width = cell.get_width()
    self._height = cell.get_height()

  # Returns a list of all the nodes touching the east side of the node
  # Sorted from smallest top value to largest
  def get_east(self):
    return self._east

  def append_east(self, node):
    if len(self._east) == 0:
      self._east.append(node)
    else:
      index = len(self._east)
      new_node_top = node.cell.get_top()
      for i in range(len(self._east)):
        other_node_top = self._east[i].cell.get_top()
        if(new_node_top < other_node_top):
          index = i
          break
      self._east.insert(index, node)

  def get_south(self):
    return self._south

  def append_south(self, node):
    if len(self._south) == 0:
      self._south.append(node)
    else:
      index = len(self._south)
      new_node_left = node.cell.get_left()
      for i in range(len(self._south)):
        other_node_left = self._south[i].cell.get_left()
        if(new_node_left < other_node_left):
          index = i
          break
      self._south.insert(index, node)

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
    self.vertical_source = Node(
      Cell(0, 0, MAX_WIDTH, 'fixed', 0, 'fixed', 'NORTH'))
    self.build_vertical_graph(self.vertical_source)
    self._all_adaptable_width_cells = None
    self._all_adaptable_height_cells = None

  def build_horizontal_graph(self, current_node):
    for other_node in self.nodes:
      if(current_node.cell.get_name() != other_node.cell.get_name()) & \
          (current_node.cell.get_right() == other_node.cell.get_left()) & \
          (current_node.cell.get_top() < other_node.cell.get_bottom()) &\
          (current_node.cell.get_bottom() > other_node.cell.get_top()): #hmmmmmm
        current_node.append_east(other_node)
    if(current_node.get_east() == []):
      return
    else:
      for east in current_node.get_east():
        self.build_horizontal_graph(east)
      return

  def build_vertical_graph(self, current_node):
    for other_node in self.nodes:
      if(current_node.cell.get_name() != other_node.cell.get_name()) & \
          (current_node.cell.get_bottom() == other_node.cell.get_top()): ## Add new constraints here!
        current_node.append_south(other_node)
    if(current_node.get_south() == []):
      return
    else:
      for south in current_node.get_south():
        self.build_vertical_graph(south)
      return

  def is_horizontal_1D(self):
    current_node = self.horizontal_source
    while(current_node.get_east() != []):
      if(len(current_node.get_east()) > 1):
        return False
      current_node = current_node.get_east()[0]
    return True

  def is_vertical_1D(self):
    current_node = self.vertical_source
    while(current_node.get_south() != []):
      if(len(current_node.get_south()) > 1):
        return False
      current_node = current_node.get_south()[0]
    return True

  # This is a function used for debugging
  def _traverse_west_to_east(self):
    current_node = self.horizontal_source
    while current_node != None:
      print(current_node.cell.get_name(), current_node.get_width())
      if current_node.get_east() != []:
        current_node = current_node.get_east()[0]
      else:
        current_node = None

  def _traverse_north_to_south(self):
    current_node = self.vertical_source
    while current_node != None:
      print(current_node.cell.get_name(), current_node.get_height())
      if current_node.get_south() != []:
        current_node = current_node.get_south()[0]
      else:
        current_node = None

  # Get the horizontal source
  def get_horizontal_source(self):
    return self.horizontal_source

  def get_vertical_source(self):
    return self.vertical_source

  # Returns a list of all adaptable cells in graph
  def get_all_adaptable_width_cells(self):
    if(self._all_adaptable_width_cells == None):
      self._all_adaptable_width_cells = []
      for current_node in self.nodes:
        if current_node.cell.w_policy == 'adaptable':
          self._all_adaptable_width_cells.append(current_node.cell)
    return self._all_adaptable_width_cells

  def get_all_adaptable_height_cells(self):
    if(self._all_adaptable_height_cells == None):
      self._all_adaptable_height_cells = []
      for current_node in self.nodes:
        if current_node.cell.h_policy == 'adaptable':
          self._all_adaptable_height_cells.append(current_node.cell)
    return self._all_adaptable_height_cells

  # Returns None if no such node exists
  def find_node(self, name):
    result = None
    for node in self.nodes:
      if(node.cell.get_name() == name):
        return node
    return result

  # This will set the width of the Node with the given name
  def set_node_width(self, name, width):
    node = self.find_node(name)
    node.set_width(width)

  def set_node_height(self, name, height):
    node = self.find_node(name)
    node.set_height(height)

# Small tests to make sure code is running correctly.
if __name__ == "__main__":
  print('Running tests for Graph.py')
  print('Test horizontal 1D')
  demo_cells = [
    Cell(0, 0, 100, 'adaptable', 100, 'adaptable', 'B'),
    Cell(0, 100, 100, 'adaptable', 100, 'adaptable', 'A'),
    Cell(0, 200, 100, 'adaptable', 100, 'adaptable', 'C'),
    Cell(0, 300, 100, 'adaptable', 100, 'adaptable', 'D')
  ]
  test_graph = Graph(demo_cells)
  print('New graph created with no issues.')
  print('Number of adaptable cells', len(test_graph.get_all_adaptable_cells()))
  print('Traverse West to East')
  test_graph._traverse_west_to_east()
  print('Test Vertical 1D')
  demo_cells = [
    Cell(0, 0, 100, 'fixed', 100, 'fixed', 'B'),
    Cell(100, 0, 100, 'fixed', 100, 'fixed', 'A'),
    Cell(200, 0, 100, 'fixed', 100, 'fixed', 'C'),
    Cell(300, 0, 100, 'fixed', 100, 'fixed', 'D')
  ]
  test_graph = Graph(demo_cells)
  print('Traverse North to South')
  print('Is vertical 1D?', test_graph.is_vertical_1D())
  print('Is horizontal 1D?', test_graph.is_horizontal_1D())
  test_graph._traverse_north_to_south()


  print('Test east node sorting')
  new_node = Node(Cell(0, 0, 100, 'adaptable', 100, 'adaptable', 'B'))
  new_node.append_east(Node(Cell(4, 100, 100, 'adaptable', 50, 'adaptable', 'C')))
  new_node.append_east(Node(Cell(50, 100, 100, 'adaptable', 50, 'adaptable', 'A')))
  new_node.append_east(Node(Cell(0, 100, 100, 'adaptable', 50, 'adaptable', 'D')))
  
  print(len(new_node.get_east()))
  for node in new_node.get_east():
    print(node.cell.get_name())
  print('Tests complete for Graph.py')
