class exception(Exception):
  def __init__(self, message, *args, metadata = None):
    self.message  = message.format(*args)
    self.metadata = metadata

class parse_error(exception):
  def __init__(self, message, line, column, filename):
    super().__init__("")
    self.message = message # cannot pass message to super constructor as that fails when report an error with token '}'
    self.line     = line
    self.column   = column
    self.filename = filename

class unknown_native_type(exception):
  def __init__(self, type):
    super().__init__("Unknown native type {}", type)

class unknown_native_function(exception):
  def __init__(self, type, name):
    super().__init__("Unknown native function {} in {}", name, type)
