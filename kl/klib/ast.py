class value:
  '''
  Represent a value in the AST (ie 1.0, "hello world"...)
  '''
  def __init__(self, value, metadata):
    self.value = value
    self.metadata = metadata
    
  def accept(self, visitor):
    return visitor.visit_value(self)

class identifier:
  '''
  Represent an identifier (ie function_name, value_name...)
  '''
  def __init__(self, identifier, metadata):
    self.identifier = identifier
    if(self.identifier == "___env___"):
      raise Exception()
    self.metadata = metadata
    
  def accept(self, visitor):
    return visitor.visit_identifier(self)

class binary_operation:
  '''
  Represent a binary operation ( + - * / && ...)
  '''
  def __init__(self, left, op, right, metadata):
    self.left = left
    self.op = op
    self.right = right
    self.metadata = metadata
    
  def accept(self, visitor):
    return visitor.visit_binary_operation(self)

class unary_operation:
  '''
  Represent an unary operation ( - ! ...)
  '''
  def __init__(self, op, right, metadata):
    self.op = op
    self.right = right
    self.metadata = metadata
    
  def accept(self, visitor):
    return visitor.visit_unary_operation(self)

class catch_expression:
  '''
  Represent a catch expression
  '''
  def __init__(self, block, catch_cond, catch_block, metadata):
    self.block        = block
    self.catch_cond   = catch_cond
    self.catch_block  = catch_block
    self.metadata     = metadata
    
  def accept(self, visitor):
    return visitor.visit_catch_expression(self)

class raise_expression:
  '''
  Represent a raise expression
  '''
  def __init__(self, expression, metadata):
    self.expression = expression
    self.metadata = metadata
    
  def accept(self, visitor):
    return visitor.visit_raise_expression(self)

class cond_expression:
  '''
  Represent a cond expression
  '''
  def __init__(self, arguments, metadata):
    self.arguments = arguments
    self.metadata = metadata
    
  def accept(self, visitor):
    return visitor.visit_cond_expression(self)

class native_call:
  '''
  Represent a call to a native function
  '''
  def __init__(self, type, name, arguments, metadata):
    self.type = type
    self.name = name
    self.arguments = arguments
    self.metadata = metadata
    
  def accept(self, visitor):
    return visitor.visit_native_call(self)

class function_call:
  '''
  Represent a call to a KL defined function
  '''
  def __init__(self, func, arguments, metadata):
    self.func = func
    self.arguments = arguments
    self.metadata = metadata
    
  def accept(self, visitor):
    return visitor.visit_function_call(self)

class lambda_declaration:
  '''
  Represent a lambda declaration (ie function (arguments) { body })
  '''
  def __init__(self, arguments, modifiers, body, metadata):
    self.arguments = arguments
    self.body = body
    self.modifiers = modifiers
    self.metadata = metadata
    
  def accept(self, visitor):
    return visitor.lambda_declaration(self)

class named_block:
  '''
  Represent a named block (ie function name(arguments) { body })
  '''
  def __init__(self, type, names, arguments, modifiers, op, body, metadata):
    self.type = type
    self.names = names
    self.arguments = arguments
    self.modifiers = modifiers
    self.op = op
    self.body = body
    self.metadata = metadata
    
  def accept(self, visitor):
    return visitor.visit_named_block(self)

class env_expression:
  '''
  Represents the "env" token
  '''
  def __init__(self, metadata):
    self.metadata = metadata
  
  def accept(self, visitor):
    return visitor.visit_env_expression(self)

class call_trace_expression:
  '''
  Represent a call to the function returning the current call_trace
  '''
  def __init__(self, metadata):
    self.metadata = metadata
  
  def accept(self, visitor):
    return visitor.visit_call_trace_expression(self)

class block_expression:
  '''
  Block expression ({ statements; })
  '''
  def __init__(self, metadata):
    self.statements = []
    self.metadata = metadata
    
  def accept(self, visitor):
    return visitor.visit_block_expression(self)

class group_expression:
  '''
  Group expression ([ statements; ])
  '''
  def __init__(self, metadata):
    self.statements = []
    self.metadata = metadata
    
  def accept(self, visitor):
    return visitor.visit_group_expression(self)

class return_expression:
  '''
  Return expression
  '''
  def __init__(self, return_value, metadata):
    self.return_value = return_value
    self.metadata = metadata
    
  def accept(self, visitor):
    return visitor.visit_return_expression(self)

class clear_expression:
  '''
  Clear expression
  '''
  def __init__(self, values, metadata):
    self.values = values
    self.metadata = metadata
    
  def accept(self, visitor):
    return visitor.visit_clear_expression(self)

class import_statement:
  '''
  Import statement
  '''
  def __init__(self, path, major_version, minor_version, metadata):
    self.path = path
    self.major_version = major_version
    self.minor_version = minor_version
    self.metadata = metadata
    
  def accept(self, visitor):
    return visitor.visit_import_statement(self)

class expression_statement:
  def __init__(self, expression, metadata):
    self.expression = expression
    self.metadata = metadata
    
  def accept(self, visitor):
    return visitor.visit_expression_statement(self)

class ast:
  '''
  Root node in the ast
  '''
  def __init__(self):
    self.statements = []
    
  def accept(self, visitor):
    return visitor.visit_ast(self)

class visitor:
  '''
  visitor in the ast
  '''
  def __init__(self):
    pass
  
  def visit_import_statement(self, node):
    raise Exception("visit_import_statement: unimplemented")

  def visit_return_expression(self, node):
    raise Exception("visit_return_expression: unimplemented")

  def visit_clear_expression(self, node):
    raise Exception("visit_clear_expression: unimplemented")

  def visit_named_block(self, node):
    raise Exception("visit_named_block: unimplemented for type {}".format(node.type))
  
  def visit_block_expression(self, node):
    raise Exception("visit_block_expression: unimplemented")
  
  def visit_group_expression(self, node):
    raise Exception("visit_group_expression: unimplemented")
  
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

  def visit_cond_expression(self, node):
    raise Exception("visit_cond_expression: unimplemented")

  def visit_catch_expression(self, node):
    raise Exception("visit_catch_expression: unimplemented")

  def visit_raise_expression(self, node):
    raise Exception("visit_raise_expression: unimplemented")

  def visit_native_call(self, node):
    raise Exception("visit_native_call: unimplemented")

  def visit_function_call(self, node):
    raise Exception("visit_function_call: unimplemented")

  def lambda_declaration(self, node):
    raise Exception("lambda_declaration: unimplemented")

  def visit_expression_statement(self, node):
    raise Exception("expression_statement: unimplemented")

  def visit_env_expression(self, node):
    raise Exception("visit_env_expression: unimplemented")

  def visit_call_trace_expression(self, node):
    raise Exception("visit_call_trace_expression: unimplemented")
