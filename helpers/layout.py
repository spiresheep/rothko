from enum import Enum
import sympy
# Local imports
from helpers.cell import Cell
from helpers.constraints import Constraint, strings_to_constraints, parse_constraints
from helpers.dimensions import get_dimensions, get_dimensions_from_graph
from helpers.dimensions import MIN_WIDTH, MIN_HEIGHT, MAX_WIDTH, MAX_HEIGHT
from helpers.graph import Graph

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
    if(self._classification != LayoutClassification.HORIZONTAL_1D):
      return
    bounds = self.determine_bounds()
    self._min_width = bounds['min_width']
    self._max_width = bounds['max_width']
    # TODO - Correct min and max_height
    self._min_height = self._current_height
    self._max_height = self._current_height

  def get_classification(self): # DONE
    return self._classification

  def get_min_width(self):
    return self._min_width

  def get_max_width(self):
    return self._max_width

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
    self._core_constraints = []
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
    self._core_constraints = core_constraints # So I don't ever have to get these constraints again
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
    # Now Solve
    symbols_list = []
    f_list = []
    for constraint in core_constraints + parse_constraints(minimizing_constraint):
      symbols_list.append(constraint.get_symbol())
      f_list.append(constraint.get_equation())
    min_solution = sympy.solve(f_list, symbols_list)
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
    # Now solve
    symbols_list = []
    f_list = []
    for constraint in core_constraints + parse_constraints(maximzing_constraint):
      symbols_list.append(constraint.get_symbol())
      f_list.append(constraint.get_equation())
    max_solution = sympy.solve(f_list, symbols_list)
    return {
      'min_width': min_solution[canvas_constraint.get_symbol()],
      'max_width': max_solution[canvas_constraint.get_symbol()]
    }

  def resize_layout(self, new_width, new_height):
    if(new_width < self._min_width):
      final_width = self._min_width
    elif(self._max_width < new_width):
      final_width = self._max_width
    else:
      final_width = new_width
    # vertical_difference = final_height - original_dimensions['height']
    match self._classification:
      case LayoutClassification.HORIZONTAL_1D:
        self.horizontal_1D_resize(final_width)
      case LayoutClassification.VERTICAL_1D:
        raise Exception('Not implimented')
      case _:
        return # do nothing!

  def horizontal_1D_resize(self, new_width):
    # Get constraints
    full_constraint_list = self._core_constraints + [Constraint(f'canvas_width = {new_width}')]
    symbols_list = []
    f_list = []
    for constraint in full_constraint_list:
      symbols_list.append(constraint.get_symbol())
      f_list.append(constraint.get_equation())
    solution = sympy.solve(f_list, symbols_list)
    print(solution)
    for key in solution:
      name = str(key).split('_')[0]
      if(name != 'canvas'):
        print('RESIZE', name, solution[key])
        self.graph.set_node_width(name, solution[key])
      if(name == 'canvas'):
        print('current canvas', solution[key])
        self._current_width = float(solution[key])
    return

  def find_node(self, name):
    self.graph.find_node_with_name(name)

if __name__ == "__main__":
  demo_cells = [
    Cell(0, 0, 100, 'fixed', 100, 'fixed', 'B'),
    Cell(0, 100, 100, 'adaptable', 100, 'adaptable', 'A'),
    Cell(0, 200, 100, 'adaptable', 100, 'adaptable', 'C'),
    Cell(0, 300, 100, 'fixed', 100, 'fixed', 'D')
  ]
  demo_constraints = []
  demo_layout = Layout(demo_cells, demo_constraints)

  demo_cells = [
    Cell(0, 0, 100, 'adaptable', 100, 'fixed', 'B'),
    Cell(0, 100, 200, 'fixed', 100, 'fixed', 'A'),
    Cell(0, 300, 300, 'constrained', 100, 'fixed', 'C'),
  ]
  demo_constraints = ['C.width = canvas.width / 2']
  demo_layout = Layout(demo_cells, strings_to_constraints(demo_constraints))
  demo_layout.resize_layout(demo_layout.get_max_width(), 100)
  demo_layout.graph.traverse_west_to_east()
