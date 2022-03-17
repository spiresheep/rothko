# hello_world.py
import json
import PySimpleGUI as sg

#export later
class Cell:
  def __init__(self, top, left, width, w_color, height, h_color, name):
    self.left = left
    self.top = top
    self.width = width
    self.height = height
    self.name = name
    #uhhhh
    self.w_color = w_color
    self.h_color = h_color
  def get_right(self):
    end = self.left + self.width
    return end

  def get_bottom(self):
    end = self.top + self.height
    return end

  def print(self):
    print(self.top, self.left, self.width, self.w_color, self.height, self.h_color, self.name)

def parse():
  print('Start parse');
  file = open('demo_file.txt', 'r')
  local = json.loads(file.read())
  cells = []
  for cell in local['cells']:
    splitH = cell["horizontal"].split(" ")
    splitV = cell["vertical"].split(" ")
    name = ""
    if "name" in cell:
      name = cell["name"]
    newCell = Cell(cell["top"], cell["left"], int(splitH[0]), splitH[1], int(splitV[0]), splitV[1], name)
    cells.append(newCell)
  print("Done parse")
  return cells

def drawCheck(cells):
  max_width = 0
  max_height = 0
  for cell in cells:
    right = cell.get_right()
    bottom = cell.get_bottom()
    if right > max_width:
      max_width = right
    if bottom > max_height:
      max_height = bottom
  return [max_width, max_height]

def draw_border(canvas, outline_width, fill, left, top, right, bottom):
  return canvas.TKCanvas.create_rectangle(left, top, right, bottom, fill=fill, width=outline_width, outline='white')

if __name__ == "__main__":
  cells_to_draw = parse()
  min_size = drawCheck(cells_to_draw)
  width = min_size[0]
  height = min_size[1]
  layout = [[sg.Canvas(size=(width, height), background_color='black', key= 'canvas')]]
  window = sg.Window('Canvas test', layout, finalize=True)
  canvas = window['canvas']
  cir = canvas.TKCanvas.create_oval(50, 50, 100, 100)
  for cell in cells_to_draw:
    left = cell.left
    right = cell.get_right()
    top = cell.top
    bottom = cell.get_bottom()
    width_color = cell.w_color
    height_color = cell.h_color
    #draw a solid color rectangle
    if cell.w_color == cell.h_color:
      if cell.w_color == 'yellow':
        canvas.TKCanvas.create_rectangle(left, top, right, bottom, fill='#ffbb00', outline='red')
      else:
        canvas.TKCanvas.create_rectangle(left, top, right, bottom, fill=cell.w_color, outline='green')
    #draw a lined rectangle
    else:
      canvas.TKCanvas.create_rectangle(left, top, right, bottom, fill='lightgrey', outline='pink')
      outline_width = 1
      border_size = 2
      #TODO better lines
      #draw blue lines 
      if width_color == 'blue':
        draw_border(canvas, outline_width, 'blue', left, top, right - outline_width, top + border_size + outline_width) #very good
        draw_border(canvas, outline_width, 'blue', left, bottom - border_size - (2 * outline_width), right - outline_width, bottom- outline_width) #crap
      if height_color == 'blue':
        draw_border(canvas, outline_width, 'blue', left, top, left + border_size + outline_width, bottom - outline_width)  #crap
        draw_border(canvas, outline_width, 'blue', right - border_size - (2 * outline_width), top, right - outline_width, bottom - outline_width)  #crap
      # #draw yellow lines #ffbb00
      if width_color == 'yellow':
        draw_border(canvas, outline_width, '#ffbb00', left, top, right - outline_width, top + border_size + outline_width) #very good
        draw_border(canvas, outline_width, '#ffbb00', left, bottom - border_size - (2 * outline_width), right - outline_width, bottom- outline_width) #crap
      if height_color == 'yellow':
        draw_border(canvas, outline_width, '#ffbb00', left, top, left + border_size + outline_width, bottom - outline_width)  #crap
        draw_border(canvas, outline_width, '#ffbb00', right - border_size - (2 * outline_width), top, right - outline_width, bottom - outline_width)  #crap
    #write text
    if cell.name != '':
      middle_height = (top + bottom) / 2
      middle_width = (left + right) / 2
      canvas.TKCanvas.create_text(middle_width, middle_height, text=cell.name, width=(right-left), fill='black')
  window.read()
