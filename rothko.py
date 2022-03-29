from helpers.parse import parse
from helpers.cell import Cell
from helpers.colors import colors
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
    outline=colors['white']
  )
  return result

def redraw(window, width, height):
  canvas = window['canvas']
  canvas.TKCanvas.configure(width=width, height=height)
  window.refresh()

def draw(canvas):
# canvas = window['canvas']
  for cell in cells_to_draw:
    left = cell.left
    right = cell.get_right()
    top = cell.top
    bottom = cell.get_bottom()
    width_color = cell.w_color()
    height_color = cell.h_color()
    #draw a solid color rectangle
    if width_color == height_color:
      canvas.TKCanvas.create_rectangle(
        left,
        top,
        right,
        bottom,
        fill=width_color,
        outline='',
        width=0
      )
    #draw a mixed policy rectangle
    else:
      outline_width = 1
      border_size = 2
      canvas.TKCanvas.create_rectangle(
        left,
        top,
        right,
        bottom,
        fill=colors['light_grey'],
        outline='',
        width=0
      )
      #draw blue lines
      if height_color == colors['blue']:
        draw_outlined_rect( #north line
          canvas, outline_width, colors['blue'],
          left, 
          top,
          right - outline_width,
          top + border_size + outline_width
        )
        draw_outlined_rect(# south line
          canvas, outline_width, colors['blue'],
          left,
          bottom - border_size - (2 * outline_width),
          right - outline_width,
          bottom - outline_width #?????
        )
      if width_color == colors['blue']:
        draw_outlined_rect(#west line
          canvas, outline_width, colors['blue'],
          left,
          top,
          left + border_size + outline_width, bottom - outline_width
        )
        draw_outlined_rect(#east line
          canvas, outline_width, colors['blue'],
          right - border_size - (2 * outline_width),
          top, right - outline_width,
          bottom - outline_width
        )
      # #draw yellow lines
      if height_color == colors['yellow']:
        draw_outlined_rect(#north line
          canvas, outline_width, colors['yellow'],
          left,
          top,
          right - outline_width,
          top + border_size + outline_width
        )
        draw_outlined_rect(#south line
          canvas, outline_width, colors['yellow'],
          left, bottom - border_size - (2 * outline_width),
          right - outline_width,
          bottom- outline_width)
      if width_color == colors['yellow']:
        draw_outlined_rect(#west line
          canvas, outline_width, colors['yellow'],
          left,
          top,
          left + border_size + outline_width,
          bottom - outline_width
        )
        draw_outlined_rect(#east line
          canvas, outline_width, colors['yellow'],
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

def make_edit_window():
  layout = [
    [sg.Text("Edit Values", key="new")],
    [sg.Text('Height'), sg.Input(key='HEIGHT')],
    [sg.Text('Width'), sg.Input(key='WIDTH')],
    [sg.Button('Update Size')]
  ]
  return sg.Window("Edit Controls", layout, finalize=True)

def make_canvas_window():
  layout = [
    [sg.Text('Source Layout File'), sg.Input(key='-sourcefile-', size=(45, 1)),
      sg.FileBrowse()],
    [sg.Button('LOAD LAYOUT', bind_return_key=True)],
    [sg.Text('Max_X: 0, Max_X: 2^24, Min_Y: 0, Max_Y: 2^24')],
    [sg.Canvas(size=(600, 100), background_color='black', key= 'canvas')]
  ]
  return sg.Window('Layout Viewer', layout, finalize=True)

if __name__ == "__main__":
  # LAYOUT DETAILS
  window1, window2 = make_canvas_window(), None
  #window = sg.Window('Canvas test', layout)
  while True:
    window, event, values = sg.read_all_windows()
    if event in ('Exit', 'Quit', None):
      break
    if event == 'LOAD LAYOUT':
      source_file = values['-sourcefile-']
      source_path, source_filename = os.path.split(source_file)
      try:
        cells_to_draw = parse(source_file)
        min_size = get_min_dimensions(cells_to_draw)
        canvas_width = min_size[0]
        canvas_height = min_size[1]
        redraw(window1, canvas_width, canvas_height)
        draw(window['canvas'])
        make_edit_window()
      except:
        cells_to_draw = []
        sg.PopupError('Something went wrong')
    if event == 'Update Size':
      new_height = values['HEIGHT']
      new_width = values['WIDTH']
      #verify if height and width are possible.... if too big revert to max, else min
      #if sizes are legit, calculate values
      redraw(window1, new_height, new_width)