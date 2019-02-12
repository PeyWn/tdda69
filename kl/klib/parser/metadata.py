class metadata:
  '''
  Metadata associated with an AST node
  '''
  def __init__(self, line, column, filename, blockname, parent):
    self.line         = line
    self.column       = column
    self.filename     = filename
    self.blockname    = blockname
    self.parent       = parent
