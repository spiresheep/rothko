from helpers.parse import parse
from helpers.cell import Cell
import PySimpleGUI as sg
import os

def get_min_dimensions(cells):
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

def draw_outlined_rect(canvas, outline_width, fill, left, top, right, bottom):
  result = canvas.TKCanvas.create_rectangle(
    left,
    top,
    right,
    bottom,
    fill=fill,
    width=outline_width,
    outline='white'
  )
  return result

if __name__ == "__main__":
  # cells_to_draw = parse('demo_file.txt')
  cells_to_draw = [
    Cell(0, 0, 100, 'blue', 100,'yellow', '')
  ]
  min_size = get_min_dimensions(cells_to_draw)
  width = min_size[0]
  height = min_size[1]

  # LAYOUT DETAILS
  layout = [
    [sg.Text('Source Layout File'), sg.Input(key='-sourcefile-', size=(45, 1)),
      sg.FileBrowse()],
    [sg.Button('Make EXE', bind_return_key=True)],
    [sg.Canvas(size=(width, height), background_color='black', key= 'canvas')]
  ]
  window = sg.Window('Canvas test', layout)
  while True:
    event, values = window.read()
    if event in ('Exit', 'Quit', None):
      break

    source_file = values['-sourcefile-']
    source_path, source_filename = os.path.split(source_file)

    if event == 'Make EXE':
      try:
        cells_to_draw = parse(source_file)
        min_size = get_min_dimensions(cells_to_draw)
        width = min_size[0]
        height = min_size[1]
        canvas = window['canvas']
        canvas.TKCanvas.configure(width=width, height=height)
        window.refresh()
      except:
        cells_to_draw = []
        sg.PopupError('Something went wrong')
    # Draw the cells
    canvas = window['canvas']
    for cell in cells_to_draw:
      left = cell.left
      right = cell.get_right()
      top = cell.top
      bottom = cell.get_bottom()
      width_color = cell.w_color
      height_color = cell.h_color
      yellow = '#ffbb00'
      #draw a solid color rectangle
      if cell.w_color == cell.h_color:
        if cell.w_color == 'yellow':
          canvas.TKCanvas.create_rectangle(
            left,
            top,
            right,
            bottom,
            fill=yellow,
            outline=''
          )
        else:
          canvas.TKCanvas.create_rectangle(
            left,
            top,
            right,
            bottom,
            fill=cell.w_color,
            outline=''
          )
      #draw a lined rectangle
      else:
        canvas.TKCanvas.create_rectangle(
          left, top, right, bottom, fill='lightgrey'
        )
        outline_width = 1
        border_size = 2
        #draw blue lines 
        if width_color == 'blue':
          draw_outlined_rect(
            canvas, outline_width, 'blue',
            left, 
            top,
            right - outline_width,
            top + border_size + outline_width
          )
          draw_outlined_rect(
            canvas, outline_width, 'blue',
            left,
            bottom - border_size - (2 * outline_width),
            right - outline_width,
            bottom - outline_width
          )
        if height_color == 'blue':
          draw_outlined_rect(
            canvas, outline_width, 'blue',
            left,
            top,
            left + border_size + outline_width, bottom - outline_width
          )
          draw_outlined_rect(
            canvas, outline_width, 'blue',
            right - border_size - (2 * outline_width),
            top, right - outline_width,
            bottom - outline_width
          )
        # #draw yellow lines
        if width_color == 'yellow':
          draw_outlined_rect(
            canvas, outline_width, '#ffbb00',
            left,
            top,
            right - outline_width,
            top + border_size + outline_width
          )
          draw_outlined_rect(
            canvas, outline_width, '#ffbb00',
            left, bottom - border_size - (2 * outline_width),
            right - outline_width,
            bottom- outline_width)
        if height_color == 'yellow':
          draw_outlined_rect(
            canvas, outline_width, '#ffbb00',
            left,
            top,
            left + border_size + outline_width,
            bottom - outline_width
          )
          draw_outlined_rect(
            canvas, outline_width, '#ffbb00',
            right - border_size - (2 * outline_width),
            top,
            right - outline_width,
            bottom - outline_width
          )
      #write text
      if cell.name != '':
        middle_height = (top + bottom) / 2
        middle_width = (left + right) / 2
        canvas.TKCanvas.create_text(
          middle_width,
          middle_height,
          text=cell.name,
          width=(right-left),
          fill='black'
        )
