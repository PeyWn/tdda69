class AccountError(Exception):
  def __init__(self, value):
    self.value = value
  def str(self):
    return repr(self.value)