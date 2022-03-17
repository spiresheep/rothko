class Cell:
  def __init__(self, top, left, width, w_color, height, h_color, name):
    self.left = left
    self.top = top
    self.width = width
    self.height = height
    self.name = name
    self.w_color = w_color
    self.h_color = h_color

  def get_right(self):
    right = self.left + self.width
    return right

  def get_bottom(self):
    bottom = self.top + self.height
    return bottom

  def print(self):
    print(self.top, self.left, self.width, self.w_color, self.height,
      self.h_color, self.name)
