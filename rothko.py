import os
import PySimpleGUI as sg
from helpers.graph import Graph, Node
from helpers.colors import colors
from helpers.dimensions import get_dimensions, get_dimensions_from_graph
from helpers.layout import Layout, LayoutClassification
from helpers.parse import parse

OUTLINE_WIDTH = 1
BORDER_SIZE = 2

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

def draw_solid_rect(canvas, fill, left, top, right, bottom):
  result = canvas.TKCanvas.create_rectangle(
    left,
    top,
    right,
    bottom,
    fill=fill,
    width=0,
    outline=colors['yellow']
  )
  return result

def canvas_resize(window, width, height):
  canvas = window['canvas']
  canvas.TKCanvas.configure(width=width, height=height)
  window.refresh()

def draw(canvas, cells_to_draw):
  for cell in cells_to_draw:
    left = cell.left
    right = cell.get_right()
    top = cell.top
    bottom = cell.get_bottom()
    width_color = cell.get_w_color()
    height_color = cell.get_h_color()
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
          bottom - outline_width #double check correctness
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

def draw_node(node):
  raise Exception('Not implimented')

def redraw_from_graph(window, layout: Layout):

  graph = layout.graph
  if(layout._classification == LayoutClassification.HORIZONTAL_1D):
    canvas = window['canvas']
    canvas_size = get_dimensions_from_graph(graph)

    canvas.TKCanvas.configure(width=canvas_size['width'], height=canvas_size['height'])
    current_node = graph.get_horizontal_source()
    current_x = 0
    current_y = 0
    while current_node != None:
      draw_node(canvas, current_x, current_y, current_node)
      if(current_node.get_east() != []):
        current_x = current_x + current_node.get_width()
        current_node = current_node.get_east()[0]
      else:
        current_node = None
  else:
    raise Exception('Format not supported')

def draw_node(canvas, x, y, node: Node):
  top = y
  left = x
  bottom = y + node.get_height()
  right = x + node.get_width()
  if(node.cell.get_w_policy() == node.cell.get_h_policy()):
    draw_solid_rect(
      canvas,
      node.cell.get_w_color(),
      x,
      y,
      right,
      bottom
    )
  elif(node.cell.get_w_policy() != node.cell.get_h_policy()):
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
    if node.cell.get_h_color() == colors['blue']:
      draw_outlined_rect( #north line
        canvas, OUTLINE_WIDTH, colors['blue'],
        left, 
        top,
        right - OUTLINE_WIDTH,
        top + BORDER_SIZE + OUTLINE_WIDTH
      )
      draw_outlined_rect(# south line
        canvas, OUTLINE_WIDTH, colors['blue'],
        left,
        bottom - BORDER_SIZE - (2 * OUTLINE_WIDTH),
        right - OUTLINE_WIDTH,
        bottom - OUTLINE_WIDTH #double check correctness
      )
    if node.cell.get_w_color() == colors['blue']:
      draw_outlined_rect(#west line
        canvas, OUTLINE_WIDTH, colors['blue'],
        left,
        top,
        left + BORDER_SIZE + OUTLINE_WIDTH, bottom - OUTLINE_WIDTH
      )
      draw_outlined_rect(#east line
        canvas, OUTLINE_WIDTH, colors['blue'],
        right - BORDER_SIZE - (2 * OUTLINE_WIDTH),
        top, right - OUTLINE_WIDTH,
        bottom - OUTLINE_WIDTH
      )
    # #draw yellow lines
    if node.cell.get_h_color() == colors['yellow']:
      draw_outlined_rect(#north line
        canvas, OUTLINE_WIDTH, colors['yellow'],
        left,
        top,
        right - OUTLINE_WIDTH,
        top + BORDER_SIZE + OUTLINE_WIDTH
      )
      draw_outlined_rect(#south line
        canvas, OUTLINE_WIDTH, colors['yellow'],
        left, bottom - BORDER_SIZE - (2 * OUTLINE_WIDTH),
        right - OUTLINE_WIDTH,
        bottom- OUTLINE_WIDTH)
    if node.cell.get_w_color() == colors['yellow']:
      draw_outlined_rect(#west line
        canvas, OUTLINE_WIDTH, colors['yellow'],
        left,
        top,
        left + BORDER_SIZE + OUTLINE_WIDTH,
        bottom - OUTLINE_WIDTH
      )
      draw_outlined_rect(#east line
        canvas, OUTLINE_WIDTH, colors['yellow'],
        right - BORDER_SIZE - (2 * OUTLINE_WIDTH),
        top,
        right - OUTLINE_WIDTH,
        bottom - OUTLINE_WIDTH
      )
  if node.cell.name != '':
    canvas.TKCanvas.create_text(
      (left + right) / 2,
      (top + bottom) / 2,
      text=node.cell.name,
      width=(right-left),
      fill='black'
    )

def render_edit_window(width, height):
  layout = [
    [sg.Text("Edit Layout", key="new")],
    [sg.Text('Width'), sg.InputText(width, key='WIDTH')],
    [sg.Text('Height'), sg.InputText(height, key='HEIGHT')],
    [sg.Button('UPDATE PREVIEW')]
  ]
  return sg.Window("Edit Controls", layout, finalize=True)

def render_layout_preview():
  layout = [
    [sg.Text('Source Layout File'), sg.Input(key='-sourcefile-', size=(45, 1)),
      sg.FileBrowse()],
    [sg.Button('LOAD LAYOUT', bind_return_key=True)],
    [sg.Text('Max_X: 0, Max_X: 2^24, Min_Y: 0, Max_Y: 2^24')],
    [sg.Canvas(size=(600, 100), background_color='black', key= 'canvas')]
  ]
  return sg.Window('Layout Viewer', layout, finalize=True)

if __name__ == "__main__":
  window1, window2 = render_layout_preview(), None
  layout = None
  while True:
    window, event, values = sg.read_all_windows()
    if event in ('Exit', 'Quit', None):
      break
    if event == 'LOAD LAYOUT':
      source_file = values['-sourcefile-']
      source_path, source_filename = os.path.split(source_file)
      try:
        cells_to_draw = parse(source_file)
        layout = Layout(cells_to_draw)
        layout_size = get_dimensions(cells_to_draw)
        canvas_resize(window1, layout_size['width'], layout_size['height'])
        draw(window['canvas'], cells_to_draw)
        if(window2 == None):
          window2 = render_edit_window(layout_size['width'], layout_size['height'])
        else:
          print('TODO - Update edit window values')
      except:
        cells_to_draw = []
        sg.PopupError('Unable to read config file.')
    if event == 'UPDATE PREVIEW':
      if(layout.get_classification() == LayoutClassification.STATIC):
        new_height = values['HEIGHT']
        new_width = values['WIDTH']
        canvas_resize(window1, new_width, new_height)
      elif(layout.get_classification() == LayoutClassification.HORIZONTAL_1D):
        new_height = values['HEIGHT']
        new_width = values['WIDTH']
        layout.resize_layout(int(new_width), int(new_height))
        redraw_from_graph(window1, layout)
      else:
        raise Exception('Not implimented')
