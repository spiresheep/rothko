from rothko.parse import parse
import PySimpleGUI as sg

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
  cells_to_draw = parse('demo_file_2.txt')
  min_size = get_min_dimensions(cells_to_draw)
  width = min_size[0]
  height = min_size[1]
  layout = [[
    sg.Canvas(size=(width, height), background_color='black', key= 'canvas')
  ]]
  window = sg.Window('Canvas test', layout, finalize=True)
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
  window.read()
