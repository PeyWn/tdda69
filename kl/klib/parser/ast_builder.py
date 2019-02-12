import klib.ast
import klib.native
import klib.exception

class ast_builder:
  '''
  Build an AST from the output of the parser
  '''
  def __init__(self):
    self.ast = klib.ast.ast()
    self.__block_stack = []
    self.__current_block = self.ast
    self.__expressions_stack = []
    
  def import_statement(self, import_name, major, minor, metadata):
    self.ast.statements.append(klib.ast.import_statement(import_name, major, minor, metadata))


  def named_block(self, block_type, block_name, arguments, modifiers, op, metadata):
    expr = None
    if(len(self.__expressions_stack) > 1):
      raise Exception("Invalid stack, should have at most one expression, but contains {} expressions".format(len(self.__expressions_stack)))
    if(len(self.__expressions_stack) == 1):
      expr = self.__expressions_stack.pop()
    self.__current_block.statements.append(klib.ast.named_block(block_type, block_name, arguments, modifiers, op, expr, metadata))
    
  def start_block_expression(self, metadata):
    self.__block_stack.append((self.__current_block, self.__expressions_stack))
    self.__expressions_stack = []
    self.__current_block = klib.ast.block_expression(metadata)

  def end_block_expression(self, metadata):
    if(len(self.__expressions_stack) != 0):
      raise Exception("Invalid stack, should be empty, but contains {} expressions".format(len(self.__expressions_stack)))
    (previous_block, previous_expression_stack) = self.__block_stack.pop()
    block = self.__current_block
    self.__current_block = previous_block
    self.__expressions_stack = previous_expression_stack
    self.__expressions_stack.append(block)

  def start_group_expression(self, metadata):
    self.__block_stack.append((self.__current_block, self.__expressions_stack))
    self.__expressions_stack = []
    self.__current_block = klib.ast.group_expression(metadata)
  
  def end_group_expression(self, metadata):
    if(len(self.__expressions_stack) != 0):
      raise Exception("Invalid stack, should be empty, but contains {} expressions".format(len(self.__expressions_stack)))
    (previous_block, previous_expression_stack) = self.__block_stack.pop()
    block = self.__current_block
    self.__current_block = previous_block
    self.__expressions_stack = previous_expression_stack
    self.__expressions_stack.append(block)

  def start_expression(self, metadata):
    pass
  
  def __check_expression_stack(self, l):
    if(len(self.__expressions_stack) < l):
      raise Exception("Invalid stack, should contains a {} expressions, but contains {} expressions".format(l, len(self.__expressions_stack)))

  def end_expression(self, metadata):
    if(len(self.__expressions_stack) != 1):
      raise Exception("Invalid stack, should contains a single expression, but contains {} expressions".format(len(self.__expressions_stack)))
    self.__current_block.statements.append(klib.ast.expression_statement(self.__expressions_stack.pop(), metadata))
  
  def clear_expression(self, arguments, metadata):
    self.__check_expression_stack(arguments)
    args = []
    for i in range(0, arguments):
      args.insert(0, self.__expressions_stack.pop())
    self.__expressions_stack.append(klib.ast.clear_expression(args, metadata))    
  
  def return_expression(self, arguments, metadata):
    self.__check_expression_stack(arguments)
    if(arguments == 1):
      self.__expressions_stack.append(klib.ast.return_expression(self.__expressions_stack.pop(), metadata))
    else:
      self.__expressions_stack.append(klib.ast.return_expression(None, metadata))
    
  def value_expression(self, value, metadata):
    self.__expressions_stack.append(klib.ast.value(value, metadata))
    
  def identifier_expression(self, identifier, metadata):
    self.__expressions_stack.append(klib.ast.identifier(identifier, metadata))

  def binary_expression(self, binop, metadata):
    self.__check_expression_stack(2)
    b = self.__expressions_stack.pop()
    a = self.__expressions_stack.pop()
    self.__expressions_stack.append(klib.ast.binary_operation(a, binop, b, metadata))
    
  def unary_expression(self, unop, metadata):
    self.__check_expression_stack(1)
    a = self.__expressions_stack.pop()
    self.__expressions_stack.append(klib.ast.unary_operation(unop, a, metadata))

  def cond_expression(self, arguments, metadata):
    self.__check_expression_stack(arguments)
    args = []
    for i in range(0, arguments):
      args.insert(0, self.__expressions_stack.pop())
    self.__expressions_stack.append(klib.ast.cond_expression(args, metadata))

  def catch_expression(self, arguments, metadata):
    self.__check_expression_stack(arguments)

    if(arguments == 2):
      catch_block = self.__expressions_stack.pop()
      catch_cond = None
      block = self.__expressions_stack.pop()
    elif(arguments == 3):
      catch_block = self.__expressions_stack.pop()
      catch_cond = self.__expressions_stack.pop()
      block = self.__expressions_stack.pop()
    else:
      raise Exception("Wrong number of arguments for catch expression.")

    self.__expressions_stack.append(klib.ast.catch_expression(block, catch_cond, catch_block, metadata))

  def raise_expression(self, metadata):
    self.__check_expression_stack(1)
    self.__expressions_stack.append(klib.ast.raise_expression(self.__expressions_stack.pop(), metadata))

  def native_call_expression(self, arguments, metadata):
    self.__check_expression_stack(2 + arguments)
    args = []
    for i in range(0, arguments):
      args.insert(0, self.__expressions_stack.pop())
    func = self.__expressions_stack.pop().value
    type = self.__expressions_stack.pop().value
    self.__expressions_stack.append(klib.ast.native_call(type, func, args, metadata))
    
  def function_call_expression(self, arguments, metadata):
    self.__check_expression_stack(1 + arguments)
    args = []
    for i in range(0, arguments):
      args.insert(0, self.__expressions_stack.pop())
    func = self.__expressions_stack.pop()
    self.__expressions_stack.append(klib.ast.function_call(func, args, metadata))

  def lambda_declaration_expression(self, arguments, modifiers, metadata):
    self.__expressions_stack.append(klib.ast.lambda_declaration(arguments, modifiers, self.__expressions_stack.pop(), metadata))

  def env_expression(self, metadata):
    self.__expressions_stack.append(klib.ast.env_expression(metadata))

  def call_trace_expression(self, metadata):
    self.__expressions_stack.append(klib.ast.call_trace_expression(metadata))
