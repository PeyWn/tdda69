
class opcode:
  '''
  Represent a single operand.
  - index is a unique number corresponding to the operand value
  - name is the name of the operand, for display purposes
  - arguments is a list of mandatory arguments for the operand
  - optional_arguments is a list of optional arguments
  - description is a documentation of the expected behavior of the operand
  '''
  def __init__(self, index, name, arguments, optional_arguments, description):
    self.index = index
    self.name = name

class binary_opcode(opcode):
  def __init__(self, index, name, description_name):
    super().__init__(index, name, [], [], "Binary operation ({}) with the two top elements from the stack".format(description_name))

class unary_opcode(opcode):
  def __init__(self, index, name, description_name):
    super().__init__(index, name, [], [], "Unary operation ({}) with the top element from the stack".format(description_name))

class opcodes:
  # Stack Manipulation
  NOP             = opcode(0, "NOP", [], [], "Do nothing")
  PUSH            = opcode(1, "PUSH", ["value"], [], "Push a constant [value] on the stack")
  POP             = opcode(2, "POP", ["count"], [], "Remove [cound] elements from the stack")
  DUP             = opcode(3, "DUP", [], [], "Duplicate the top value on the stack")
  SWAP            = opcode(4, "SWAP", [], [], "Swap the top two members of the stack")
  
  # Environment and objects manipulation
  PUSH_ENV        = opcode(10, "PUSH_ENV", [], [], "Push the environment on the stack")
  NEW_ENV         = opcode(11, "NEW_ENV", [], [], "Create a new environment and set it as the current environment")
  DROP_ENV        = opcode(12, "DROP_ENV", [], [], "Drop the current environment")
  MAKE_REF        = opcode(13, "MAKE_REF", [], ["name"], "Create a reference (if no name is sepcified 2: environment 1: name otherwise 1: environment)")
  STORE           = opcode(14, "STORE", [], ["name"], "Take a value from the stack and store it in the reference (if no name is specified 2: reference 1: value, otherwise 1: value and the value is stored in the current environment)")
  DCL_CELL        = opcode(15, "DCL_CELL", ["name"], [], "Declare a new cell called [varname]")
  DEF_VALUE       = opcode(16, "DEF_VALUE", ["name"], [], "Define a new value [varname] take the value from the stack")
  CLEAR           = opcode(17, "CLEAR", [], ["name"], "Clear the value [name] from the top environment from the stack")
  PUSH_CALL_TRACE = opcode(18, "PUSH_CALL_TRACE", [], [], "Push call trace on the stack")
  
  # Control
  JMP             = opcode(20, "JMP", ["index"], [], "Jump to a specific [index]")
  IFJMP           = opcode(21, "IFJMP", ["index"], [], "Jump to a specific [index] if top value on the stack is true")
  UNLESSJMP       = opcode(22, "UNLESSJMP", ["index"], [], "Jump to a specific [index] if top value on the stack is false")
  NATIVE_CALL     = opcode(23, "NATIVE_CALL", ["name", "count"], [], "Call a native function [name] with [count] arguments from the stack")
  CALL            = opcode(24, "CALL", ["count"], [], "Call the function from the top of the stack with [count] number of arguments (n: arg n-1 1: argument 0 0: function object )")
  RET             = opcode(25, "RET", [], [], "Return from a function call")

  # Exceptions
  TRY_PUSH        = opcode(30, "TRY_PUSH", ["index"], [], "Push [index] to jump to if an exception is thrown.")
  TRY_POP         = opcode(31, "TRY_POP", [], [], "Pop exception index.")
  THROW           = opcode(32, "THROW", [], [], "Throw an exception, with the first object of the stack.")
  
  # Array and Objects creation
  MAKE_FUNC       = opcode(40, "MAKE_FUNC", ["body", "argument_names", "modifiers"], [], "Make a function with [body], [argument_names] and [modifiers]")
  
  # Binary arithmetic operation
  ADD             = binary_opcode(50, "ADD", "addition")
  MUL             = binary_opcode(51, "MUL", "multiplication")
  SUB             = binary_opcode(52, "SUB", "subtraction")
  DIV             = binary_opcode(53, "DIV", "division")
  MOD             = binary_opcode(54, "MOD", "modulo")
  LEFT_SHIFT      = binary_opcode(55, "LEFT_SHIFT", "left shift")
  RIGHT_SHIFT     = binary_opcode(56, "RIGHT_SHIFT", "right shift")
  UNSIGNED_RIGHT_SHIFT  = binary_opcode(57, "UNSIGNED_RIGHT_SHIFT", "unsigned right shift")
  
  # Binary bolean operation
  GREATER         = binary_opcode(60, "GREATER", "superior")
  GREATER_EQUAL   = binary_opcode(61, "GREATER_EQUAL", "superior or equal")
  LESS            = binary_opcode(62, "LESS", "inferior")
  LESS_EQUAL      = binary_opcode(63, "LESS_EQUAL", "inferior or equal")
  EQUAL           = binary_opcode(64, "EQUAL", "equal")
  DIFFERENT       = binary_opcode(65, "DIFFERENT", "different")
  AND             = binary_opcode(66, "AND", "and")
  OR              = binary_opcode(67, "OR", "or")

  # Unary operations
  NEG             = unary_opcode(70, "NEG", "negation")
  TILDE           = unary_opcode(71, "TILDE", "complement")
  NOT             = unary_opcode(72, "NOT", "not")
