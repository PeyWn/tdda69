
class print_listener:
  '''
  Listen to the output of the parser and print
  '''
  def __init__(self, ostream):
    self.ostream = ostream

  def import_statement(self, import_name, major, minor, metadata):
    self.ostream.writeln("import_statement: {} {}.{}", import_name, major, minor)

  def named_block(self, block_type, block_name, arguments, modifiers, op, metadata):
    self.ostream.writeln("named_block: {} {} {}", block_type, block_name, op)
    for arg in arguments:
      self.ostream.writeln("  argument: {}", arg)
    for mod in modifiers:
      self.ostream.writeln("  modifiers: {}", mod)
  
  def end_block(self, metadata):
    self.ostream.writeln("end_block")

  def start_block_expression(self, metadata):
    self.ostream.writeln("start_block_expression")

  def end_block_expression(self, metadata):
    self.ostream.writeln("end_block_expression")

  def start_group_expression(self, metadata):
    self.ostream.writeln("start_group_expression")

  def end_group_expression(self, metadata):
    self.ostream.writeln("end_group_expression")

  def start_expression(self, metadata):
    self.ostream.writeln("start_expression")

  def end_expression(self, metadata):
    self.ostream.writeln("end_expression")

  def end_expression(self, metadata):
    self.ostream.writeln("end_expression")

  def clear_expression(self, arguments, metadata):
    self.ostream.writeln("clear_expression: {}", arguments)

  def return_expression(self, arguments, metadata):
    self.ostream.writeln("return_expression: {}", arguments)

  def value_expression(self, identifier, metadata):
    self.ostream.writeln("value_expression: {}", identifier)

  def identifier_expression(self, identifier, metadata):
    self.ostream.writeln("identifier_expression: {}", identifier)

  def binary_expression(self, binop, metadata):
    self.ostream.writeln("binary_expression: {}", binop)

  def unary_expression(self, unop, metadata):
    self.ostream.writeln("unary_expression: {}", unop)
    
  def cond_expression(self, arguments, metadata):
    self.ostream.writeln("cond_expression: {}", arguments)
    
  def catch_expression(self, arguments, metadata):
    self.ostream.writeln("catch_expression: {}", arguments)
    
  def call_trace_expression(self, metadata):
    self.ostream.writeln("call_trace_expression")
    
  def native_call_expression(self, arguments, metadata):
    self.ostream.writeln("native_call_expression: {}", arguments)

  def function_call_expression(self, arguments, metadata):
    self.ostream.writeln("function_call_expression: {}", arguments)

  def lambda_declaration_expression(self, arguments, modifiers, metadata):
    self.ostream.writeln("lambda_declaration_expression")
    for arg in arguments:
      self.ostream.writeln("  argument: {}", arg)
    for mod in modifiers:
      self.ostream.writeln("  modifiers: {}", mod)
    
  def env_expression(self, metadata):
    self.ostream.writeln("env_expression")

  def raise_expression(self, metadata):
    self.ostream.writeln("raise_expression")
