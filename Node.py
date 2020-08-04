import numpy

class Node:

  def __init__(self, kind, val):
    self.kind = kind
    self.val = val
    self.children = []
    self.parent = None

    # init number of children
    if val == 'and' or val == 'or':
      self.children = [None, None]
    elif val == 'not':
      self.children = [None]
    elif val == 'if':
      self.children = [None, None, None]
    else: # Terminal
      self.children = None

  def __str__(self):
    print(self.val)

  