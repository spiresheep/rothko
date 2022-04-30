from enum import Enum
import sympy
from helpers.cell import Cell
from helpers.constraints import Constraint
from helpers.dimensions import get_dimensions, get_dimensions_from_graph
from helpers.dimensions import MAX_WIDTH, MAX_HEIGHT
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
    self._constraints = constraints
    current_size = get_dimensions(cells)
    self._current_width = current_size['width']
    self._current_height = current_size['height']
    self.graph = Graph(cells)
    # Generate some extra data about the layout - immutable properties - to cut
    # down on repetitive work.
    self._min_width = self._current_width
    self._max_width = self._current_width
    self._min_height = self._current_height
    self._max_height = self._current_height
    self._classification = self._determine_classification()
    self._core_constraints = self.generate_core_constraints(constraints)
    bounds = self.solve_core_for_min_max()
    self._min_width = bounds['min_width']
    self._max_width = bounds['max_width']
    self._min_height = bounds['min_height']
    self._max_height = bounds['max_height']

  def get_classification(self): # DONE
    return self._classification

  def get_min_width(self):
    return float(self._min_width)

  def get_max_width(self):
    return float(self._max_width)

  def get_min_height(self):
    return float(self._min_height)

  def get_max_height(self):
    return float(self._max_height)

  # Helper function that computes the type of layout
  def _determine_classification(self): # DONE
    is_horizontal = self.graph.is_horizontal_1D()
    is_vertical = self.graph.is_vertical_1D()
    if(is_horizontal & is_vertical):
      return LayoutClassification.HORIZONTAL_1D
    if(is_horizontal):
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
        return self._get_1D_horizontal_get_width_bounds()
      case LayoutClassification.HORIZONTAL_1D:
        return self._get_1D_horizontal_get_width_bounds()
      case LayoutClassification.VERTICAL_1D:
        return self._get_1D_vertical_get_height_bounds()

  def solve_core_for_min_max(self): #junk atm
    symbols_list = []
    f_list = []
    for constraint in self._core_constraints:
      symbols_list.append(constraint.get_symbol())
      f_list.append(constraint.get_equation())
    solution = sympy.solve(f_list, symbols_list)
    return_values = {
      'min_width': 0,
      'max_width': MAX_HEIGHT,
      'min_height': 0,
      'max_height': MAX_HEIGHT,
    }
    solution = sympy.solve(f_list, symbols_list)
    print(solution)
    for key in solution:
      if(str(key) == 'canvas_width'):
        return_values['min_width'] = solution[key]
        return_values['max_width'] = solution[key]
      else:
        print('solve for min max')
      if(str(key) == 'canvas_height'):
        return_values['min_height'] = solution[key]
        return_values['max_height'] = solution[key]
      else:
        print('solve for min max')
    print('return_values', return_values)
    return return_values

  def generate_core_constraints(self, constraints):
    core = [
      Constraint(f'MAX_WIDTH = {MAX_WIDTH}')
    ]
    for cell in self.graph.get_all_fixed_height_cells():
      cell_name = cell.get_name()
      core.append(Constraint(f'{cell_name}_height={cell.get_height()}'))
    for cell in self.graph.get_all_fixed_width_cells():
      cell_name = cell.get_name()
      core.append(Constraint(f'{cell_name}_width={cell.get_width()}'))
    for cell in self.graph.get_all_adaptable_width_cells():
      cell_name = cell.get_name()
      core.append(Constraint(f'{cell_name}_width={cell_name}_width'))
    for cell in self.graph.get_all_adaptable_height_cells():
      cell_name = cell.get_name()
      core.append(Constraint(f'{cell_name}_height={cell_name}_height'))
    core = core + self.get_width_constraints()
    core = core + self.get_height_constraints()
    # Need to add one more type of constraint <_<
   
    #check constraints
    print('~~~~Core Constraints Here')
    for constraint in core:
      print(constraint._left, '=', constraint._right)
    symbols_list = []
    f_list = []
    for constraint in core:
      symbols_list.append(constraint.get_symbol())
      f_list.append(constraint.get_equation())
    solution = sympy.solve(f_list, symbols_list)
    print(solution)
    canvas_width_min_not_max = True
    canvas_height_min_not_max = True
    for key in solution:
      if(str(key) == 'canvas_width'):
        print('key', key)
        print('omg solution')
        canvas_width_min_not_max = False
      if(str(key) == 'canvas_height'):
        canvas_height_min_not_max = False
    # WIP
    if canvas_width_min_not_max:
      print('Width is under constrained')
    else:
      print('min width = max_wdith')
    if canvas_height_min_not_max:
      print('Height is under constrained')
    #WIP
    return core

  def get_width_constraints(self):
    source = self.graph.get_horizontal_source()
    new_constraints = []
    for node in source.get_east():
      symbols = self.get_width_symbols(node)
      print(symbols)
      rhs = ''
      for symbol in symbols:
        if len(rhs) != 0:
          rhs = rhs + '+' + str(symbol)
        else:
          rhs = str(symbol)
      print(f'canvas_width = {rhs}')
      new_constraints.append(Constraint(f'canvas_width={rhs}'))
    return new_constraints

  def get_width_symbols(self, node):
    result = [f'{node.cell.get_name()}_width']
    print(result)
    if(node.get_east() != []):
      result = result + self.get_width_symbols(node.get_east()[0])
    return result

  def get_height_constraints(self):
    source = self.graph.get_vertical_source()
    new_constraints = []
    for node in source.get_south():
      symbols = self.get_height_symbols(node)
      print(symbols)
      rhs = ''
      for symbol in symbols:
        if len(rhs) != 0:
          rhs = rhs + '+' + str(symbol)
        else:
          rhs = str(symbol)
      print(f'canvas_height = {rhs}')
      new_constraints.append(Constraint(f'canvas_height={rhs}'))
    return new_constraints

  def get_height_symbols(self, node):
    result = [f'{node.cell.get_name()}_height']
    print(result)
    if(node.get_south() != []):
      result = result + self.get_height_symbols(node.get_south()[0])
    return result

  def apply_solution_to_graph(self, solution):
    print('update graph')
    for key in solution:
      key_as_string = str(key)
      if key_as_string.count('_') == 2:
        split_key = key_as_string.rsplit('_',1)
      else:
        split_key = key_as_string.split('_')
      name = split_key[0]
      property = split_key[1]
      print('thing', name, property)
      if(name != 'canvas') & (name != 'MAX'):
        if(property == 'height'):
          self.graph.set_node_height(name, solution[key])
        if(property == 'width'):
          self.graph.set_node_width(name, solution[key])

  def resize_layout(self, new_width, new_height):
    if(new_width < self._min_width):
      final_width = self._min_width
    elif(self._max_width < new_width):
      final_width = self._max_width
    else:
      final_width = new_width
    if(new_height < self._min_height):
      final_height = self._min_height
    elif(self._max_height < new_height):
      final_height = self._max_height
    else:
      final_height = new_height
    # vertical_difference = final_height - original_dimensions['height']
    match self._classification:
      case LayoutClassification.HORIZONTAL_1D:
        self._resize(final_width, final_height)
      case LayoutClassification.VERTICAL_1D:
        self._resize(final_width, final_height)
      case _:
        return # do nothing!
    size = get_dimensions_from_graph(self.graph)
    self._current_height = size['height']
    self._current_width = size['width']

  def _resize(self, new_width, new_height):
    full_constraint_list = self._core_constraints + \
      [Constraint(f'canvas_height = {new_height}'), Constraint(f'canvas_width = {new_width}')]
    symbols_list = []
    f_list = []
    for constraint in full_constraint_list:
      symbols_list.append(constraint.get_symbol())
      f_list.append(constraint.get_equation())
    solution = sympy.solve(f_list, symbols_list)
    # for key in solution:
    #   print(float(solution[key]))
    self.apply_solution_to_graph(solution)  
    return 

  def find_node(self, name):
    self.graph.find_node_with_name(name)

if __name__ == "__main__":
  demo_cells = [
    Cell(0, 0, 100, 'adaptable', 100, 'adaptable'),
    # Cell(0, 100, 100, 'fixed', 100, 'fixed', 'A')
  ]
  demo_constraints = []
  demo_layout = Layout(demo_cells, demo_constraints)
  # demo_cells = [
  #   Cell(0, 0, 100, 'fixed', 100, 'fixed', 'B'),
  #   Cell(100, 0, 100, 'adaptable', 100, 'adaptable', 'A'),
  #   Cell(200, 0, 100, 'adaptable', 100, 'adaptable', 'C'),
  #   Cell(300, 0, 100, 'fixed', 100, 'fixed', 'D')
  # ]
  # demo_constraints = []
  # demo_layout = Layout(demo_cells, demo_constraints)
  # demo_cells = [
  #   Cell(0, 0, 100, 'fixed', 100, 'fixed', 'B'),
  #   Cell(100, 0, 100, 'adaptable', 100, 'adaptable', 'A'),
  #   Cell(0, 100, 100, 'adaptable', 100, 'adaptable', 'C'),
  #   Cell(100, 100, 100, 'fixed', 100, 'fixed', 'D')
  # ]
  # demo_constraints = []
  # demo_layout = Layout(demo_cells, demo_constraints)
  # demo_cells = [
  #   Cell(0, 0, 100, 'adaptable', 100, 'fixed', 'B'),
  #   Cell(0, 100, 200, 'fixed', 100, 'fixed', 'A'),
  #   Cell(0, 300, 300, 'constrained', 100, 'fixed', 'C'),
  # ]
  # demo_constraints = ['C.width = canvas.width / 2']
  # demo_layout = Layout(demo_cells, strings_to_constraints(demo_constraints))
  # demo_layout.resize_layout(demo_layout.get_max_width(), 100)
  # demo_layout.graph._traverse_west_to_east()
