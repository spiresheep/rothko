import os
import PySimpleGUI as sg
from helpers.graph import Graph, Node
from helpers.colors import colors
from helpers.dimensions import MAX_HEIGHT, MAX_WIDTH, get_dimensions, get_dimensions_from_graph
from helpers.layout import Layout, LayoutClassification
from helpers.parse_from_json import parse

# The size of the border for mixed policy cells
BORDER_SIZE = 2
# The size of the outline of the border
OUTLINE_WIDTH = 1 

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

def resize_canvas(window, width, height):
  canvas = window['drawing_area']
  canvas.TKCanvas.configure(width=width, height=height)
  window.refresh()

def draw_from_layout(canvas, layout: Layout):
  graph = layout.graph
  if(layout._classification == LayoutClassification.HORIZONTAL_1D):
    canvas.TKCanvas.configure(
      width=layout._current_width,
      height=layout._current_height
    )
    current_node = graph.get_horizontal_source()
    current_x = 0
    current_y = 0
    while current_node != None:
      if(current_node.get_width() != 0):
        draw_node(canvas, current_x, current_y, current_node)
      if(current_node.get_east() != []):
        current_x = current_x + current_node.get_width()
        current_node = current_node.get_east()[0]
      else:
        current_node = None
  else:
    raise Exception('Format not supported')

# Function that draws a single cell of a layout from a node
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
    #draw green lines
    if node.cell.get_h_color() == colors['green']:
      draw_outlined_rect( #north line
        canvas, OUTLINE_WIDTH, colors['green'],
        left, 
        top,
        right - OUTLINE_WIDTH,
        top + BORDER_SIZE + OUTLINE_WIDTH
      )
      draw_outlined_rect(# south line
        canvas, OUTLINE_WIDTH, colors['green'],
        left,
        bottom - BORDER_SIZE - (2 * OUTLINE_WIDTH),
        right - OUTLINE_WIDTH,
        bottom - OUTLINE_WIDTH #double check correctness
      )
    if node.cell.get_w_color() == colors['green']:
      draw_outlined_rect(#west line
        canvas, OUTLINE_WIDTH, colors['green'],
        left,
        top,
        left + BORDER_SIZE + OUTLINE_WIDTH, bottom - OUTLINE_WIDTH
      )
      draw_outlined_rect(#east line
        canvas, OUTLINE_WIDTH, colors['green'],
        right - BORDER_SIZE - (2 * OUTLINE_WIDTH),
        top, right - OUTLINE_WIDTH,
        bottom - OUTLINE_WIDTH
      )
    #draw yellow lines
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
  if node.cell.public_name() != '':
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

def render_layout_preview_window():
  window_layout = [
    [sg.Text('Source Layout File'), sg.Input(key='-sourcefile-', size=(45, 1)),
      sg.FileBrowse()],
    [sg.Button('LOAD LAYOUT', bind_return_key=True)],
    [sg.Text(f'Min Width: 0, Max Width: {MAX_WIDTH}, Min Height: 0, \
      Max Height: {MAX_HEIGHT}', key='-min-and-max-')],
    [sg.Canvas(size=(600, 100), background_color='black', key='drawing_area')]
  ]
  return sg.Window('Layout Viewer', window_layout, finalize=True)

if __name__ == "__main__":
  window1, window2 = render_layout_preview_window(), None
  layout = None
  while True:
    window, event, values = sg.read_all_windows()
    if event in ('Exit', 'Quit', None):
      break
    if event == 'LOAD LAYOUT':
      source_file = values['-sourcefile-']
      source_path, source_filename = os.path.split(source_file)
      layout = parse(source_file)
      resize_canvas(window1, layout._current_width, layout._current_height)
      draw_from_layout(window['drawing_area'], layout)
      if(window2 != None):
        window2.close()
      window1['-min-and-max-'].update(f'Min Width: {layout._min_width:.1f} Max Width: {layout._max_width:.1f}')
      window2 = render_edit_window(layout._current_width, layout._current_height)
    if event == 'UPDATE PREVIEW':
      if(layout.get_classification() == LayoutClassification.STATIC):
        new_height = values['HEIGHT']
        new_width = values['WIDTH']
        resize_canvas(window1['drawing_area'], new_width, new_height)
      elif(layout.get_classification() == LayoutClassification.HORIZONTAL_1D):
        new_height = values['HEIGHT']
        new_width = values['WIDTH']
        layout.resize_layout(float(new_width), float(new_height))
        draw_from_layout(window1['drawing_area'], layout)
      else:
        raise Exception('Not implimented')
