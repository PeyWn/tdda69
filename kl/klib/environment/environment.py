from .cell  import cell
from .value     import value, undefined_value

import klib.exception

class unknown_cell(klib.exception):
  def __init__(self, cell):
    super().__init__("Unknown cell '{}'", cell)

class already_defined_cell(klib.exception):
  def __init__(self, cell):
    super().__init__("Already defined cell '{}'", cell)

class environment:
  """
  Environment class used to define cells and values.
  """
  
  def __init__(self, parent = None):
    """
    Initialise an environment. The parent is an other environment
    where value for cells can be looked up recursively.
    """
    self.parent     = parent
    self.__cvs  = {}
  
  def define_value(self, name, init_value = undefined_value, init_binding = undefined_value, init_binding_environment = None):
    if(name in self.__cvs):
      raise already_defined_cell(name)
    v = value(name, init_value = init_value, init_binding = init_binding, init_binding_environment = init_binding_environment)
    self.__cvs[name] = v
  
  def define_cell(self, name, init_value = undefined_value, init_binding = undefined_value, init_binding_environment = None):
    """
    Create a new cell with the name "name" and the initial value
    "init".
    """
    if(name in self.__cvs):
      raise already_defined_cell(name)
    v = cell(name, init_value = init_value, init_binding = init_binding, init_binding_environment = init_binding_environment)
    self.__cvs[name] = v
  
  def get(self, name):
    """
    Get the value of a cell. If the cell is not defined in
    this environment, it should look in the parent environment.
    If it is not found in the root environment, it should raise the
    exception Utils.UnknownVariable.
    """
    if(name in self.__cvs):
      return self.__cvs[name]
    elif(self.parent != None):
      return self.parent.get(name)
    else:
      raise unknown_cell(name)

  def clear(self, name):
    del self.__cvs[name]

  def __len__(self):
    return len(self.__cvs)
