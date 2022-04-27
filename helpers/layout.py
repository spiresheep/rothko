from enum import Enum
import sympy
# Local imports
from cell import Cell
from constraints import Constraint, strings_to_constraints, parse_constraints
from dimensions import get_dimensions, get_dimensions_from_graph
from dimensions import MIN_WIDTH, MIN_HEIGHT, MAX_WIDTH, MAX_HEIGHT
from graph import Graph

# Categorization of layouts to make it easier to reason about them
class LayoutClassification(Enum):
  EMPTY = 0
  SINGLE_CELL = 1
  HORIZONTAL_1D = 2
  VERTICAL_1D = 3
  STATIC = 4

# A layout contains all the data needed to display and modify a layout
class Layout:
  def __init__(self, cells, constraints=[]):
    self.initial_cells = cells
    # Canvas is the current size of the layout
    current_size = get_dimensions(cells)
    self._current_width = current_size['width']
    self._current_height = current_size['height']
    # Build the graph!
    self.graph = Graph(cells)
    # Using the graph and constraint_strings calculate min and max size
    self._constraints = constraints
    # Generate some extra data about the layout - immutable properties - to cut
    # down on repetitive work.
    self._classification = self._determine_classification()
    # Now can get min and max_width
    # print('Min and Max', self.determine_bounds())
    bounds = self.determine_bounds()
    self._min_width = bounds['min_width']
    self._max_width = bounds['max_width']

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
        return self._get_1D_horizontal_min_and_max()
      case LayoutClassification.HORIZONTAL_1D:
        return self._get_1D_horizontal_min_and_max()
      case LayoutClassification.VERTICAL_1D:
        raise Exception('Not implimented')

  def _get_1D_horizontal_min_and_max(self):
    fixed_constraints = []
    adaptable_cells = self.graph.get_all_adaptable_cells()
    # Generate constraints from fixed cells
    current_node = self.graph.get_horizontal_source()
    while (current_node != None):
      if (current_node.cell.w_policy == 'fixed') & (current_node.cell.name != 'WEST'):
        fixed_constraints.append(f'{current_node.cell.name}_width = {current_node.cell.width}')
      if (current_node.get_east() != []):
        current_node = current_node.get_east()[0]
      else:
        current_node = None
    # Generate the adaaptable cell constraints
    adaptable_constrains = []
    if(len(adaptable_cells) == 1):
      first_cell = adaptable_cells[0]
      cell_name = adaptable_cells[0].get_name()
      adaptable_constrains.append(f'{cell_name}_width = {cell_name}_width')
    elif(len(adaptable_cells) > 1):
      first_cell = adaptable_cells[0]
      first_cell_name = adaptable_cells[0].get_name()
      for other_cell in adaptable_cells:
        constraint = (f'{other_cell.get_name()}_width = {first_cell_name}' + 
          f'_width*({other_cell.get_width()}/{first_cell.get_width()})')
        adaptable_constrains.append(constraint)
    # Add these constraints if we need them...
    base_constaints = []
    for constraint in fixed_constraints + adaptable_constrains:
      if 'MAX_WIDTH' in constraint:
        base_constaints = [f'MAX_WIDTH = {MAX_WIDTH}']
        break
    core_constraints = parse_constraints(base_constaints + fixed_constraints + adaptable_constrains) + self._constraints
    # Generate the canvas constraint
    rhs = ''
    for constraint in core_constraints:
      if((str(constraint.get_symbol()) != 'MAX_WIDTH') & (str(constraint.get_symbol()) != 'MIN_WIDTH')):
        if len(rhs) != 0:
          rhs = rhs + '+' + str(constraint.get_symbol())
        else:
          rhs = str(constraint.get_symbol())
    width_constraint = f'canvas_width = {rhs}'
    canvas_constraint = Constraint(width_constraint)
    core_constraints.append(canvas_constraint)
    # Minimized adaptable cells
    minimizing_constraint = []
    if(len(adaptable_cells) >= 1):
      cell_name = adaptable_cells[0].get_name()
      minimizing_constraint.append(f'{cell_name}_width = 0')
    #NOW SOLVE <3
    symbols_list = []
    f_list = []
    for constraint in core_constraints + parse_constraints(minimizing_constraint):
      symbols_list.append(constraint.get_symbol())
      f_list.append(constraint.get_equation())
    min_solution = sympy.solve(f_list, symbols_list)
    # print('flist', f_list)
    # print('symbols_list', symbols_list)
    # print('~~Minimum Solution~~', min_solution)
    # Maximize adaptable cells
    maximzing_constraint = []
    if(len(adaptable_cells) >= 1):
      cell_name = adaptable_cells[0].get_name()
      current_node = self.graph.get_horizontal_source()
      # Get constraints from fixed cells and adaptable cells
      rhs = ''
      while (current_node != None):
        if (current_node.cell.get_name() != cell_name) & (current_node.cell.get_name() != 'WEST'):
          name = current_node.cell.name + '_width'
          if len(rhs) != 0:
            rhs = rhs + '-' + name
          else:
            rhs = name
        if (current_node.get_east() != []):
          current_node = current_node.get_east()[0]
        else:
          current_node = None
      maximzing_constraint.append(f'{cell_name}_width = {MAX_WIDTH} - {rhs}')
      # print('~~MAXIMIZING CONSTRAINT~~', maximzing_constraint)
    #NOW SOLVE <3
    symbols_list = []
    f_list = []
    for constraint in core_constraints + parse_constraints(maximzing_constraint):
      symbols_list.append(constraint.get_symbol())
      f_list.append(constraint.get_equation())
    #remove symbol duplicates
    max_solution = sympy.solve(f_list, symbols_list)
    # print('flist', f_list)
    # print('symbols_list', symbols_list)
    # print('~~Maximum Solution~~', max_solution[canvas_constraint.get_symbol()])
    return {
      'min_width': min_solution[canvas_constraint.get_symbol()],
      'max_width': max_solution[canvas_constraint.get_symbol()]
    }

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
    self.graph.find_node_with_name(name)

  def set_size_of_node(self, node, name, property):
    raise Exception('Not implimented')

if __name__ == "__main__":
  demo_cells = [
    Cell(0, 0, 100, 'fixed', 100, 'fixed', 'B'),
    Cell(0, 100, 100, 'adaptable', 100, 'adaptable', 'A'),
    Cell(0, 200, 100, 'adaptable', 100, 'adaptable', 'C'),
    Cell(0, 300, 100, 'fixed', 100, 'fixed', 'D')
  ]
  demo_constraints = []
  Layout(demo_cells, demo_constraints)

  demo_cells = [
    Cell(0, 0, 100, 'adaptable', 100, 'fixed', 'B'),
    Cell(0, 100, 200, 'fixed', 100, 'fixed', 'A'),
    Cell(0, 300, 300, 'constrained', 100, 'fixed', 'C'),
  ]
  demo_constraints = ['C.width = canvas.width / 2']
  Layout(demo_cells, strings_to_constraints(demo_constraints))
