from helpers.colors import convert_policy_to_color

# Data about a single rectangle within the layout.
class Cell:
  def __init__(self, top, left, width, w_policy, height, h_policy, name):
    self._left = left
    self._top = top
    self._width = width
    self._height = height
    self._name = name
    self._w_policy = w_policy
    self._h_policy = h_policy

  def get_name(self):
    return self._name;

  def get_top(self):
    return self._top

  def set_top(self, top):
    self._top = top

  def get_left(self):
    return self._left

  def set_left(self, left):
    self._left = left

  def get_width(self):
    return self._width

  def get_height(self):
    return self._height

  #calculated
  def get_right(self):
    right = self._left + self._width
    return right

  #calculated
  def get_bottom(self):
    bottom = self._top + self._height
    return bottom

  def get_h_policy(self):
    return self._h_policy

  def get_w_policy(self):
    return self._w_policy

  def get_h_color(self):
    return convert_policy_to_color(self._h_policy)

  def get_w_color(self):
    return convert_policy_to_color(self._w_policy)

  def clone(self):
    return Cell(
      self._top,
      self._left,
      self._width,
      self._w_policy,
      self._height,
      self._h_policy,
      self._name
    )

  name=property(get_name)
  top=property(get_top)
  left=property(get_left)
  width=property(get_width)
  height=property(get_height)
  h_policy=property(get_h_policy)
  w_policy=property(get_w_policy)
