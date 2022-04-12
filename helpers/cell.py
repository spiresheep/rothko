from helpers.colors import convert_policy_to_color

# Data about a single rectangle within the layout.
class Cell:
  def __init__(self, top, left, width, w_policy, height, h_policy, name):
    self.left = left
    self.top = top
    self.width = width
    self.height = height
    self.name = name
    self.w_policy = w_policy
    self.h_policy = h_policy
    self.min_size = 0
    self.max_size = 0

  def get_name(self):
    return self.name;

  # Document
  def get_top(self):
    return self.top;

  def set_top(self, top):
    self.top = top

  # Document
  def get_left(self):
    return self.left

  def set_left(self, left):
    self.left = left

  def get_width(self):
    return self.width

  def get_height(self):
    return self.height;

  #calculated
  def get_right(self):
    right = self.left + self.width
    return right

  #calculated
  def get_bottom(self):
    bottom = self.top + self.height
    return bottom

  def get_h_policy(self):
    return self.h_policy

  def get_w_policy(self):
    return self.w_policy

  def get_h_color(self):
    return convert_policy_to_color(self.h_policy)

  def get_w_color(self):
    return convert_policy_to_color(self.w_policy)

  def clone(self):
    return Cell(
      self.top,
      self.left,
      self.width,
      self.w_policy,
      self.height,
      self.h_policy,
      self.name
    )

  name=property(get_name)
  top=property(get_top)
  left=property(get_left)
  width=property(get_width)
  height=property(get_height)
  h_policy=property(get_h_policy)
  w_policy=property(get_w_policy)

  def print(self):
    print('Starting Point', self.top, self.left,
      'Width and Policy',self.width, self.w_policy, self.height, self.h_policy, 
      'Name', self.name)
