
class reference:
  '''
  A reference represent a value stored in an environment
  '''
  def __init__(self, environment, name):
    self.environment  = environment
    self.name         = name
  def __str__(self):
    return "({}.{})".format(self.environment, self.name)
