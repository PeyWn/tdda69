import klib.math

import klib.environment

from klib.bytecode import opcodes
from .stack   import stack
from klib.io import stdout
import klib.interpreter.kl_exception


class executor_context:
  def __init__(self, program, environment):
    self.program          = program
    self.environment      = environment
    self.current_index    = 0
    self.stack            = stack()
    self.exceptions_stack = stack()

class exception_context:
  def __init__(self, index):
    self.index = index

class call_trace():
  def __init__(self, trace):
    self.trace = trace

class executor:

  opmaps = {}

  def __init__(self):
    self.current_context = None
    self.execution_stack = stack()

    if(len(executor.opmaps) == 0):
      # Stack
      executor.opmaps[opcodes.PUSH] = executor.execute_push
      executor.opmaps[opcodes.POP] = executor.execute_pop
      executor.opmaps[opcodes.DUP] = executor.execute_dup
      executor.opmaps[opcodes.SWAP] = executor.execute_swap
      executor.opmaps[opcodes.PUSH_ENV] = executor.execute_push_env
      executor.opmaps[opcodes.NEW_ENV] = executor.execute_new_env
      executor.opmaps[opcodes.DROP_ENV] = executor.execute_drop_env
      executor.opmaps[opcodes.MAKE_REF] = executor.execute_make_ref
      executor.opmaps[opcodes.STORE] = executor.execute_store
      executor.opmaps[opcodes.DCL_CELL] = executor.dcl_cell
      executor.opmaps[opcodes.DEF_VALUE] = executor.def_value
      executor.opmaps[opcodes.CLEAR] = executor.clear
      executor.opmaps[opcodes.PUSH_CALL_TRACE] = executor.push_call_trace
      executor.opmaps[opcodes.JMP] = executor.jmp
      executor.opmaps[opcodes.IFJMP] = executor.ifjmp
      executor.opmaps[opcodes.RET] = executor.ret
      executor.opmaps[opcodes.NATIVE_CALL] = executor.native_call
      executor.opmaps[opcodes.CALL] = executor.call
      executor.opmaps[opcodes.TRY_PUSH] = executor.try_push
      executor.opmaps[opcodes.TRY_POP] = executor.try_pop
      executor.opmaps[opcodes.THROW] = executor.throw
      executor.opmaps[opcodes.MAKE_FUNC] = executor.make_func
      executor.opmaps[opcodes.ADD] = executor.ADD
      executor.opmaps[opcodes.SUB] = executor.SUB
      executor.opmaps[opcodes.MUL] = executor.MUL
      executor.opmaps[opcodes.DIV] = executor.DIV
      executor.opmaps[opcodes.MOD] = executor.MOD
      executor.opmaps[opcodes.LEFT_SHIFT] = executor.LEFT_SHIFT
      executor.opmaps[opcodes.RIGHT_SHIFT] = executor.RIGHT_SHIFT
      executor.opmaps[opcodes.UNSIGNED_RIGHT_SHIFT] = executor.UNSIGNED_RIGHT_SHIFT
      executor.opmaps[opcodes.GREATER] = executor.GREATER
      executor.opmaps[opcodes.GREATER_EQUAL] = executor.GREATER_EQUAL
      executor.opmaps[opcodes.LESS] = executor.LESS
      executor.opmaps[opcodes.LESS_EQUAL] = executor.LESS_EQUAL
      executor.opmaps[opcodes.EQUAL] = executor.EQUAL
      executor.opmaps[opcodes.DIFFERENT] = executor.DIFFERENT
      executor.opmaps[opcodes.AND] = executor.AND
      executor.opmaps[opcodes.OR] = executor.OR
      executor.opmaps[opcodes.NEG] = executor.NEG
      executor.opmaps[opcodes.TILDE] = executor.TILDE
      executor.opmaps[opcodes.NOT] = executor.NOT


  def execute(self, program, environment = klib.environment.environment(), caller_metadata = None, return_stack = False ,verbose = True):
    self.current_context = executor_context(program, environment)
    self.caller_metadata = caller_metadata
    self.ct = call_trace([])

    if verbose:
      program.print()

    while(self.current_context.current_index < len(self.current_context.program.instructions)):

      inst = self.current_context.program.instructions[self.current_context.current_index]

      if verbose:
        stdout.writeln("===== In context level: {}", len(self.execution_stack))
        stdout.write("{}: {} ({})", self.current_context.current_index, inst.opcode.name, inst.opcode.index)
        for k in inst.params:
          stdout.write(" {}={}", k, inst.params[k])
        stdout.writeln("")

        self.current_context.stack.print()

      f = executor.opmaps[inst.opcode]

      self.ct.trace.append(self.current_context)

      r = f(self, **inst.params)

      if r:
        return r

      self.current_context.current_index += 1

    if(len(self.execution_stack) != 0):
      raise Exception("execution stack is not empty")

    if(len(self.current_context.stack) > 0):
      return self.__pop_value()

    if return_stack:
      return self.current_context.stack


  def __pop_value(self):
    ret = []
    for elem in range(0, self.current_context.stack.__len__()):
      ret = [self.current_context.stack.pop()] + ret
    return ret

  def execute_push(self, value):
    self.current_context.stack.push(value)

  def execute_dup(self):
    self.current_context.stack.dup()

  def execute_swap(self):
    self.current_context.stack.swap()

  def execute_pop(self, count = 1):
    for i in range(0, count):
      self.current_context.stack.pop()

  def execute_push_env(self):
    self.current_context.stack.push(self.current_context.environment)

  def execute_new_env(self):
    self.current_context.environment = klib.environment.environment(self.current_context.environment)

  def execute_drop_env(self):
    self.current_context.environment = self.current_context.environment.parent

  def execute_make_ref(self, name = None):
    if name is None:
      name = self.current_context.stack.pop()
    env = self.current_context.stack.pop()
    self.current_context.stack.push(klib.environment.reference(env, name))

  def execute_store(self, name = None):
    elem = self.current_context.stack.pop()

    if isinstance(elem, klib.environment.reference):
      elem = elem.environment.get(elem.name)
      while isinstance(elem, klib.environment.reference):
        elem = elem.environment.get(elem.name)
      value = elem.get_value()
    else:
      value = elem

    if name is None:
      ref = self.current_context.stack.pop()
      name = ref.name
      env = ref.environment
    else:
      env = self.current_context.stack.pop()

    env.get(name).set_value(value)
    self.current_context.stack.push(value)

  def dcl_cell(self, name = None):
    env = self.current_context.stack.pop()
    env.define_cell(name)

  def def_value(self, name = None):
    value = self.current_context.stack.pop()
    env = self.current_context.stack.pop()
    env.define_value(name, value)

  def clear(self, name = None):
    elem = self.current_context.stack.pop()
    if isinstance(elem, klib.environment.reference):
      name = elem.name
      env = elem.environment
    else:
      env = elem

    while env.parent is not None:
      env = env.parent

    env.clear(name)
    self.current_context.stack.push(None)

  def push_call_trace(self):
    self.current_context.stack.push([klib.parser.metadata(self.ct.trace.pop().current_index, 0, None, None, None)])

  def jmp(self, index = None):
    if index is not None:
      self.current_context.current_index = index - 1

  def ifjmp(self, index = None):
    if self.current_context.stack.pop():
      self.jmp(index)

  def ret(self):
    elem = self.current_context.stack.pop()

    if isinstance(elem, klib.environment.reference):
      elem = elem.environment.get(elem.name)
      while isinstance(elem, klib.environment.reference):
        elem = elem.environment.get(elem.name)
      value = elem.get_value()
    else:
      value = elem
    return value

  def native_call(self, native_function = None, count = 0):
    args = []
    for i in range(0, count):
      args.append(self.current_context.stack.pop())
    self.current_context.stack.push(native_function(args)[0])

  def call(self, count = 0):
    args = []
    funcy = self.current_context.stack.pop()
    print(funcy)
    for i in range(0, count):
      args.append(self.current_context.stack.pop())
    new_env, new_prog = funcy.prepare_call(args)
    ret = self.execute(new_prog, new_env, return_stack = True)
    self.current_context.stack.push(ret[0])

  def try_push(self, index = 0):
    self.current_context.exceptions_stack.push(index)

  def try_pop(self):
    self.current_context.exceptions_stack.pop()

  def throw(self):
    if self.current_context.exceptions_stack.__len__() > 0:
      self.current_context.current_index = self.current_context.exceptions_stack.pop()
    else:
      raise klib.interpreter.kl_exception(self.current_context.current_index)

  def make_func(self, body = None, argument_names = None, modifiers = None):
    func = klib.environment.function(argument_names, body, self.current_context.environment)
    self.current_context.stack.push(func)

  def ADD(self):
    r = self.current_context.stack.pop()
    l = self.current_context.stack.pop()
    self.current_context.stack.push(l + r)

  def SUB(self):
    r = self.current_context.stack.pop()
    l = self.current_context.stack.pop()
    self.current_context.stack.push(l - r)

  def MUL(self):
    r = self.current_context.stack.pop()
    l = self.current_context.stack.pop()
    self.current_context.stack.push(l * r)

  def DIV(self):
    r = self.current_context.stack.pop()
    l = self.current_context.stack.pop()
    self.current_context.stack.push(l / r)

  def MOD(self):
    r = self.current_context.stack.pop()
    l = self.current_context.stack.pop()
    self.current_context.stack.push(l % r)

  def LEFT_SHIFT(self):
    r = int(self.current_context.stack.pop())
    l = int(self.current_context.stack.pop())
    self.current_context.stack.push(l << r)

  def RIGHT_SHIFT(self):
    r = int(self.current_context.stack.pop())
    l = int(self.current_context.stack.pop())
    self.current_context.stack.push(l >> r)

  def UNSIGNED_RIGHT_SHIFT(self):
    r = int(self.current_context.stack.pop())
    l = int(self.current_context.stack.pop())
    self.current_context.stack.push(l + 0x100000000 >> r)

  def GREATER(self):
    r = self.current_context.stack.pop()
    l = self.current_context.stack.pop()
    self.current_context.stack.push(l > r)

  def GREATER_EQUAL(self):
    r = self.current_context.stack.pop()
    l = self.current_context.stack.pop()
    self.current_context.stack.push(l >= r)

  def LESS(self):
    r = self.current_context.stack.pop()
    l = self.current_context.stack.pop()
    self.current_context.stack.push(l < r)

  def LESS_EQUAL(self):
    r = self.current_context.stack.pop()
    l = self.current_context.stack.pop()
    self.current_context.stack.push(l <= r)

  def EQUAL(self):
    r = self.current_context.stack.pop()
    l = self.current_context.stack.pop()
    self.current_context.stack.push(l == r)

  def DIFFERENT(self):
    r = self.current_context.stack.pop()
    l = self.current_context.stack.pop()
    self.current_context.stack.push(not(l == r))

  def AND(self):
    r = self.current_context.stack.pop()
    l = self.current_context.stack.pop()
    self.current_context.stack.push(l and r)

  def OR(self):
    r = int(self.current_context.stack.pop())
    l = int(self.current_context.stack.pop())
    self.current_context.stack.push(l or r)

  def NEG(self):
    elem = self.current_context.stack.pop()
    self.current_context.stack.push(-elem)

  def TILDE(self):
    elem = int(self.current_context.stack.pop())
    self.current_context.stack.push(~elem)

  def NOT(self):
    elem = self.current_context.stack.pop()
    self.current_context.stack.push( not elem)
