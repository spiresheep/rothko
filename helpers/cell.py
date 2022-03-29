from helpers.colors import convert_policy_to_color

class Cell:
  def __init__(self, top, left, width, w_rule, height, h_rule, name):
    self.left = left
    self.top = top
    self.width = width
    self.height = height
    self.name = name
    self.w_rule = w_rule
    self.h_rule = h_rule
    self.min_size = 0
    self.max_size = 0

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

  def h_policy(self):
    return self.h_rule

  def w_policy(self):
    return self.w_rule

  #calculated
  def get_right(self):
    right = self.left + self.width
    return right

  #calculated
  def get_bottom(self):
    bottom = self.top + self.height
    return bottom

  def h_color(self):
    return convert_policy_to_color(self.h_rule)

  def w_color(self):
    return convert_policy_to_color(self.w_rule)

  def clone(self):
    return Cell(
      self.top,
      self.left,
      self.width,
      self.w_rule,
      self.height,
      self.h_rule,
      self.name
    )

  def print(self):
    print(self.top, self.left, self.width, self.w_rule, self.height,
      self.h_rule, self.name)
