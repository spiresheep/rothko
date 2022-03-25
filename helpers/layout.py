from helpers.cell import Cell

MIN_WIDTH = 0
MIN_HEIGHT = 0
MAX_WIDTH = 2^24
MAX_HEIGHT = 2^24

# Node class
class Node:
  def __init__(self, cell):
    self.cell = cell
    east = []

  def get_east(self):
    return self.east.copy()

# Graph Class
class Graph:
  def __init__(self, cells):
    self.nodes = []
    for cell in cells:
      self.nodes.append(Node(cell))
    size = self.current_size()
    self.horizontal_source = Node(
      Cell(0, 0, 0, 'fixed', size['current_height'], 'fixed', 'WEST'))
    self.build_horizontal_graph(self.horizontal_source)

  def build_horizontal_graph(self, current_node):
    for node in self.nodes:
      if(current_node.get_right == node.get_left):
        current_node.east.append(node)
    if(node.east == []):
      return
    else:
      for east in self.current_node.east:
        self.build_horizontal_graph(east)
      return

  #returns a positive number if it can shrink and by how much
  def can_horizontal_shrink(self):
    widths = self.get_all_lengths(self.horizontal_source, 0)
    current_width = self.curret_size('current_width')
    biggest_length = widths[0]
    for width in widths:
      if(width > biggest_length):
        current_width = width
    return max(current_width - biggest_length, 0)

  # helper function, returns a list of widths
  def get_all_min_widths(self, current_node, total):
    if(current_node.east == []):
      if(current_node.cell.get_width_rule() == 'fixed'):
        return total + current_node.cell.get_width()
      else:
        return total
    else:
      lengths = {}
      for node in current_node.east:
        tail_total = self.get_all_min_widths(node, total)
        if(current_node.cell.get_width_rule() == 'fixed'):
          return current_node.cell.get_width() + tail_total
        else:
          return tail_total
      return lengths
    }

#fjksfkldkls
 #returns a positive number if it can grow and by how much
  def can_horizontal_grow(self):
    widths = self.get_all_lengths(self.horizontal_source, MAX_WIDTH)
    current_width = self.curret_size('current_width')
    smallest_length = widths[0]
    for width in widths:
      if(width < smallest_length):
        current_width = width
    return max(smallest_length - current_width, 0)

  # helper function, returns a list of widths
  def get_all_max_widths(self, current_node, total):
    if(current_node.east == []):
      if(current_node.cell.get_width_rule() == 'fixed'):
        return ###???
      else:
        return ###????
    lengths = {}
    for node in current_node.east:
      lengths.append(self.can_horizontal_shrink(node, total))
    return lengths

#sdfdsfdsfds

  #helper to get the current size of the layout
  def current_size(self):
    max_width = 0
    max_height = 0
    for node in self.nodes:
      right = node.cell.get_right()
      bottom = node.get_bottom()
      if right > max_width:
        max_width = right
      if bottom > max_height:
        max_height = bottom
    return {
      'current_width': max_width,
      'current_height': max_height
    }

  def get_cells_from_graph():
    return Exception('return a list plz')

#The nodes
class Layout:
  def __init__(self, cells):
    print('create layout')
    self.h_grow = 'unknown'
    self.h_shrink = 'unknown'
    self.graph = Graph(cells)

  #returns none or a layout
  def horizontal_shrink(self):
    if(self.h_grow == 'unknown'):
      shrinkage = self.graph.can_horizontal_shrink()
      if(shrinkage > 0):
        self.h_grow = Layout([])
      else:
        self.h_grow = None
    return self.h_grow