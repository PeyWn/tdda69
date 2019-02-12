
class instruction:
  '''
  Represent a single instruction with its given op_code and its parameters
  '''
  def __init__(self, opcode, metadata, **params):
    self.opcode   = opcode
    self.params   = params
    self.metadata = metadata
