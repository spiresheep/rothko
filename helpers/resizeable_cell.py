from helpers.cell import Cell

class ResizeableCell:
  def __init__(self, cell):
    self.cell = cell

  def get_name(self):
    return self.cell.name;

  def get_top(self):
    return self.cell.top;

  def top_left(self):
    return self.cell.left;

  def get_width(self):
    return self.cell.width;

  def get_height(self):
    return self.cell.height;

  def get_right(self):
    return self.cell.get_right()

  def get_bottom(self):
    return self.cell.get_bottom()

  # other useful tasks
  def has_horizontal_slack(self, cells):
    return False

  def has_vertical_slack(self, cells):
    return False

