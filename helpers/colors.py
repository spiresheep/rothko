colors = {
  'white': '#FFFFFF',
  'black':'#000000',
  'error': '#FF5800',
  'yellow': '#FFBB00',
  'blue': '#0066FF',
  'light_grey': '#F5F5F5'
}

def convert_policy_to_color(policy):
  if(policy == 'fixed'):
    return colors['yellow']
  if(policy == 'adaptable'):
    return colors['blue']
  else:
    return colors['error']