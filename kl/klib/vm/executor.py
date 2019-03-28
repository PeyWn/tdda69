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

  def execute(self, program, environment = klib.environment.environment(), caller_metadata = None, return_stack = False ,verbose = True):
    self.current_context = executor_context(program, environment)
    self.caller_metadata = caller_metadata

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

      r = f(self, **inst.params)

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

  def execute_make_ref(self, name = 'name'):
    klib.environment.reference(self.current_context.environment, name)

  def execute_store(self, name = 'name'):
    klib.environment.reference(self.current_context.environment, name)
    self.current_context.stack.pop()
