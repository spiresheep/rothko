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

  def get_right(self):
    right = self.left + self.width
    return right

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
