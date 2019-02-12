from klib.event import event
from klib.ast import visitor as ast_visitor
import klib.exception

from .function import function

class unset_value_exception(Exception):
  def __init__(self, name):
    super().__init__("Access to unset cell '{}'", name)

class listen_cell_changed(ast_visitor):
  def __init__(self):
    pass
  def visit_import_statement(self, node):
    raise Exception("visit_import_statement: unimplemented")

  def visit_return_expression(self, node):
    raise Exception("visit_return_expression: unimplemented")

  def visit_named_block(self, node):
    raise Exception("visit_named_block: unimplemented")
  
  def visit_block_expression(self, node):
    raise Exception("visit_block_expression: unimplemented")
  
  def visit_statements(self, statements):
    for statement in statements:
      statement.accept(self)
  def visit_ast(self, node):
    self.visit_statements(node.statements)
  def visit_value(self, node):
    raise Exception("visit_value: unimplemented")
  def visit_identifier(self, node):
    raise Exception("visit_identifier: unimplemented")
  def visit_binary_operation(self, node):
    raise Exception("visit_binary_operation: unimplemented")
  def visit_unary_operation(self, node):
    raise Exception("visit_unary_operation: unimplemented")
  def visit_function_call(self, node):
    raise Exception("visit_function_call: unimplemented")
  def lambda_declaration(self, node):
    raise Exception("lambda_declaration: unimplemented")

class undefined_value:
  pass

class value:
  '''
  Represent a value stored in an environment
  name is the name of the value
  init_value is the initial value
  '''
  def __init__(self, name, init_value = undefined_value, init_binding = undefined_value, init_binding_environment = None, cell = False):
    if init_value == undefined_value and init_binding == undefined_value and not cell:
      raise unset_value_exception(self.name)
    self.up_to_date = False
    if init_value != undefined_value:
      self.value = init_value
      self.up_to_date = True
    else:
      self.value = None

    if init_binding != undefined_value:
      self.binding  = function([], init_binding, init_binding_environment)
      self.binding.accept(listen_cell_changed(self.out_dated))
    else:
      self.binding = None

    self.name = name
    self.changed = event()

  def is_writable(self):
    return False
    
  def get_value(self):
    if self.up_to_date:
      return self.value
    elif self.binding:
      self.value = self.binding.call()
      self.up_to_date = True
      return self.value
    else:
      raise unset_value_exception(self.name)

  def out_dated(self):
    if not self.up_to_date:
      self.up_to_date = False
      self.changed.trigger()
    
