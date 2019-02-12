from .value import value, undefined_value
from .function import function

class cell(value):
  '''
  Implementation of a cell (aka a state)
  '''
  def __init__(self, name, init_value = undefined_value, init_binding = undefined_value, init_binding_environment = None):
    super().__init__(name, init_value = init_value, init_binding = init_binding, init_binding_environment = init_binding_environment, cell = True)

  def is_writable(self):
    return True

  def set_value(self, value):
    if(value == self):
      raise Exception()
    self.value    = value
    self.binding  = None
    self.up_to_date = True
    self.changed.trigger()
  
  def set_binding(self, binding, env):
    self.value    = None
    self.binding  = function([], binding, env)
    self.binding.accept(listen_cell_changed(self.out_dated))
    self.up_to_date = False
    self.changed.trigger()
