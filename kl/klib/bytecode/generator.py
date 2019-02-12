from klib.ast import visitor as ast_visitor
from klib.parser import binary_operator, unary_operator
import klib.exception
import klib.environment

from .program import program
from .opcodes  import opcodes
from .instruction import instruction

binary_operator_opcodes = {
    binary_operator.Addition:       opcodes.ADD,
    binary_operator.Substraction:   opcodes.SUB,
    binary_operator.Multiplication: opcodes.MUL,
    binary_operator.Division:       opcodes.DIV,
    binary_operator.Remainder:      opcodes.MOD,
    binary_operator.ShiftLeft:      opcodes.LEFT_SHIFT,
    binary_operator.ShiftRight:     opcodes.RIGHT_SHIFT,
    binary_operator.LogicalAnd:     opcodes.AND,
    binary_operator.LogicalOr:      opcodes.OR,
    binary_operator.Equal:          opcodes.EQUAL,
    binary_operator.NotEqual:       opcodes.DIFFERENT,
    binary_operator.Less:           opcodes.LESS,
    binary_operator.Greater:        opcodes.GREATER,
    binary_operator.LessEqual:      opcodes.LESS_EQUAL,
    binary_operator.GreaterEqual:   opcodes.GREATER_EQUAL
  }

class bytecode_generation_exception(klib.exception):
  def __init__(self, message, *args):
    super().__init__(message, *args)

class generator(ast_visitor):
  '''
  Class that generates a bytecode program based on a AST representation of KL
  '''
  def __init__(self):
    self.__program = program()

  def __add_instruction(self, opcode_, metadata, **arguments):
    if opcode_ == opcodes.PUSH:
        if(arguments["value"] == "___env___"):
          raise Exception()
    inst = instruction(opcode_, metadata, **arguments)
    self.__program.add_instruction(inst)
    return inst

  def finalise_program(self):
    self.__add_instruction(opcodes.PUSH, None, value = None)
    self.__add_instruction(opcodes.RET, None)
    return self.__program

  def visit_import_statement(self, node):
    raise Exception("visit_import_statement: unimplemented")

  def visit_return_expression(self, node):
    if(node.return_value):
      node.return_value.accept(self)
    else:
      self.__add_instruction(opcodes.PUSH, node.metadata, value = None)
    self.__add_instruction(opcodes.RET, node.metadata)      

  def visit_named_block(self, node):
    self.__add_instruction(opcodes.PUSH_ENV, node.metadata)
    for i in range(0, len(node.names) - 1):
      self.__add_instruction(opcodes().MAKE_REF, node.metadata, name = node.names[i])
    
    if(node.type == "___define___"):
      node.body.accept(self)
      self.__add_instruction(opcodes.DEF_VALUE, node.metadata, name = node.names[-1])
    elif(node.type == "___cell___"):
      if node.body:
        self.__add_instruction(opcodes.DUP, node.metadata)
      self.__add_instruction(opcodes.DCL_CELL, node.metadata, name = node.names[-1])
      if node.body:
        node.body.accept(self)
        self.__add_instruction(opcodes.STORE, node.metadata, name = node.names[-1])
        self.__add_instruction(opcodes.POP, node.metadata)
    else:
      raise Exception("visit_named_block: unimplemented for node type {}", node.type)
  
  def visit_block_expression(self, node):
    self.__add_instruction(opcodes.NEW_ENV, node.metadata)
    for s in node.statements:
      s.accept(self)
    self.__add_instruction(opcodes.PUSH_ENV, node.metadata)
    self.__add_instruction(opcodes.DROP_ENV, node.metadata)
  
  def visit_group_expression(self, node):
    for s in node.statements:
      s.accept(self)
    self.__add_instruction(opcodes.PUSH, node.metadata, value = None)
  
  def visit_statements(self, statements):
    for statement in statements:
      statement.accept(self)

  def visit_ast(self, node):
    self.visit_statements(node.statements)

  def visit_value(self, node):
    self.__add_instruction(opcodes.PUSH, node.metadata, value = node.value)

  def visit_identifier(self, node):
    self.__add_instruction(opcodes.PUSH, node.metadata, value=klib.environment.reference(None, node.identifier))
  
  def visit_binary_operation(self, node):
    if node.op == binary_operator.Member:
      node.left.accept(self)
      node.right.accept(self)
      self.__add_instruction(opcodes.MAKE_REF, node.metadata, name=None)
    else:
      if node.op == binary_operator.Assignment:
        node.left.accept(self)
        node.right.accept(self)
        self.__add_instruction(opcodes.STORE, node.metadata, name=None)
      else:
        node.left.accept(self)
        node.right.accept(self)
        opc = binary_operator_opcodes[node.op]
        self.__add_instruction(opc, node.metadata)
  
  def visit_unary_operation(self, node):
    node.right.accept(self)
    if(node.op == unary_operator.LogicalNegation):
      self.__add_instruction(opcodes.NOT, node.metadata)
    elif(node.op == unary_operator.AdditiveInverse):
      self.__add_instruction(opcodes.NEG, node.metadata)
    elif(node.op == unary_operator.Tilde):
      self.__add_instruction(opcodes.TILDE, node.metadata)
    elif(node.op == unary_operator.Identity):
      pass
    else:
      raise Exception("visit_unary_operation: unimplemented")

  def visit_catch_expression(self, node):
    #if(node.catch_cond):
      #node.catch_cond.accept(self)
    #else:
      #self.__add_instruction(opcodes.PUSH, node.metadata, value = None)
    
    # Execute block
    try_push_i = self.__add_instruction(opcodes.TRY_PUSH, node.metadata, index = 0)
    node.block.accept(self)
    # Remove the exception from the exception stack
    self.__add_instruction(opcodes.TRY_POP, node.metadata)
    # Jump to after the catch statement
    jmp_i = self.__add_instruction(opcodes.JMP, node.metadata)
    # This is the exception handling
    try_push_i.params["index"] = self.__program.current_index()
    # Handle condition
    if(node.catch_cond):
      # Duplicate the exception value, since it might be gobbled by the function call
      self.__add_instruction(opcodes.DUP, node.metadata)
      node.catch_cond.accept(self)
      if(self.__program.instructions[-1].opcode == opcodes.MAKE_FUNC):
        self.__add_instruction(opcodes.CALL, node.metadata, count = 1)
      else:
        # Remove the duplicated exception value
        self.__add_instruction(opcodes.SWAP, node.metadata)
        self.__add_instruction(opcodes.POP, node.metadata)

      self.__add_instruction(opcodes.IFJMP, node.metadata, index = self.__program.current_index() + 2) # we accept the exception, jump after the throw
      self.__add_instruction(opcodes.THROW, node.metadata) # Rethrow the exception
      
    node.catch_block.accept(self)
    if(self.__program.instructions[-1].opcode == opcodes.MAKE_FUNC):
      self.__add_instruction(opcodes.CALL, node.metadata, count = 1)
    else:
      # Remove the exception value
      self.__add_instruction(opcodes.POP, node.metadata)
    jmp_i.params["index"] = self.__program.current_index()
    
  def visit_raise_expression(self, node):
    node.expression.accept(self)
    self.__add_instruction(opcodes.THROW, node.metadata)

  def visit_clear_expression(self, node):
    for arg in node.values:
      arg.accept(self)
      self.__add_instruction(opcodes.CLEAR, node.metadata, name = None)

  def visit_cond_expression(self, node):
    current_index = 0
    jumps = []
    while current_index + 1 < len(node.arguments):
      node.arguments[current_index].accept(self)
      ifi         = self.__add_instruction(opcodes.UNLESSJMP, node.metadata)
      node.arguments[current_index+1].accept(self)
      jumps.append(self.__add_instruction(opcodes.JMP, node.metadata))
      ifi.params["index"] = self.__program.current_index()
      current_index += 2
    
    if current_index == len(node.arguments) - 1:
      node.arguments[current_index].accept(self)
    else:
      self.__add_instruction(opcodes.PUSH, node.metadata, value = None)
    
    for j in jumps:
      j.params["index"] = self.__program.current_index()
    
  def visit_native_call(self, node):
    for a in node.arguments:
      a.accept(self)
      
    module = klib.native.modules[node.type]
    if module:
      native_function = module.get(node.name)
    else:
      raise klib.exception.unknown_native_type(node.type)
    if not native_function:
      raise klib.exception.unknown_native_function(node.type, node.name)
    self.__add_instruction(opcodes.NATIVE_CALL, node.metadata, native_function = native_function, count = len(node.arguments))
  
  def visit_function_call(self, node):
    for a in node.arguments:
      a.accept(self)
    node.func.accept(self)
    self.__add_instruction(opcodes.CALL, node.metadata, count = len(node.arguments))

  def lambda_declaration(self, node):
    import klib.environment.utils as ki_utils
    self.__add_instruction(opcodes.MAKE_FUNC, node.metadata, body = node.body, argument_names = node.arguments, modifiers = ki_utils.function_modifiers(node))

  def visit_expression_statement(self, node):
    node.expression.accept(self)
    self.__add_instruction(opcodes.POP, node.metadata)

  def visit_env_expression(self, node):
    self.__add_instruction(opcodes.PUSH_ENV, node.metadata)

  def visit_call_trace_expression(self, node):
    self.__add_instruction(opcodes.PUSH_CALL_TRACE, node.metadata)
