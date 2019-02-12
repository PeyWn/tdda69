import klib.io

class abort_exception(Exception):
  def __init__(self, message, stack_trace):
    super().__init__(message)
    self.stack_trace = stack_trace

class __python:
  '''
  Interface with python
  '''
  def assert_(self, check, stack_trace = []):
    if not check:
      raise abort_exception("Failure", stack_trace)
  def abort(self, message = "", stack_trace = []):
    raise abort_exception(message, stack_trace)
  def print(self, text):
    klib.io.stdout.writeln(str(text))
  def identity(self, value):
    return value
  def get(self, name):
    if(hasattr(self, name)):
      return getattr(self, name)
    else:
      return None

python = __python()
