from enum import Enum
from helpers.graph import Graph
from helpers.cell import Cell
from helpers.dimensions import get_dimensions, get_dimensions_from_graph
from helpers.dimensions import MIN_WIDTH, MIN_HEIGHT, MAX_WIDTH, MAX_HEIGHT

# Categorization of layouts to make it easier to reason about them
class LayoutClassification(Enum):
  EMPTY = 0
  SINGLE_CELL = 1
  HORIZONTAL_1D = 2
  VERTICAL_1D = 3
  STATIC = 4

# A layout contains all the data needed to display and modify a layout
class Layout:
  def __init__(self, cells, constraints=None):
    self.initial_cells = cells
    # These initial values are not the final values
    # The min and max values might be better defaults.
    bounds = get_dimensions(cells)
    canvas_width = bounds['width']
    canvas_height = bounds['height']
    self.min_width = canvas_width
    self.max_width = canvas_width
    self.min_height = canvas_height
    self.max_height = canvas_height
    self.graph = Graph(cells)
    self.graph.traverse_west_to_east()
    self._constraints = constraints
    # Generate some extra data about the layout - immutable properties - to cut
    # down on repetitive work.
    self._classification = self._determine_classification()


  # Helper function that computes the type of layout
  def _determine_classification(self): # DONE
    is_horizontal = self.graph.is_horizontal_1D()
    is_vertical = False # TODO - Add test for this
    if(is_horizontal and is_vertical):
      return LayoutClassification.SINGLE_CELL
    elif(is_horizontal):
      return LayoutClassification.HORIZONTAL_1D
    elif(is_vertical):
      return LayoutClassification.VERTICAL_1D
    else:
      return LayoutClassification.STATIC

  def get_classification(self): # DONE
    return self._classification

  def determine_bounds(self):
    match self._classification:
      case LayoutClassification.STATIC:
        return # TODO - Later
      case LayoutClassification.SINGLE_CELL:
        raise Exception('Not implimented')
      case LayoutClassification.HORIZONTAL_1D:
        # TODO - Now
        raise Exception('Not implimented')
      case LayoutClassification.VERTICAL_1D:
        raise Exception('Not implimented')

  def resize_layout(self, new_width, new_height):
    raise Exception('Not implimented')
    # if(new_width < self.min_width):
    #   final_width = self.min_width
    # elif(self.max_width < new_width):
    #   final_width = self.max_width
    # else:
    #   final_width = new_width
    # original_dimensions = get_dimensions_from_graph(self.graph)
    # horizontal_difference = final_width - original_dimensions['width']
    # # vertical_difference = final_height - original_dimensions['height']
    # match self._classification:
    #   case LayoutClassification.HORIZONTAL_1D:
    #     self.horizontal_1D_resize(horizontal_difference)
    #   case LayoutClassification.VERTICAL_1D:
    #     raise Exception('Not implimented')
    #   case _:
    #     return # do nothing!

  def horizontal_1D_resize(self, change: float):
    if(change == 0):
      return
    nodes_to_resize = []
    current_node = self.graph.get_horizontal_source()
    while(current_node!= None):
      if(current_node.cell.get_w_policy() == 'adaptable'):
        nodes_to_resize.append(current_node)
      if(current_node.get_east() != []):
        current_node = current_node.get_east()[0]
      else:
        current_node = None
    if(len(nodes_to_resize) > 0):
      difference = change / len(nodes_to_resize)
    else:
      return
    for node in nodes_to_resize:
      node.set_width(node.get_width() + difference)

  def find_node(self, name):
    self.graph.findName(name)

  def set_size_of_node(self, node, name, property):
    raise Exception('Not implimented')