import klib.exception
import klib.environment
import klib.bytecode

class invalid_arguments_exception(klib.exception):
  def __init__(self, expected, got):
    super().__init__("Invalid number of arguments, expected {} got {}", expected, got)

class function:
  '''
  Represent a function.
  argument_names represent a list of arguments
  body is an AST representation of the body of the function
  environment is the environment where the function was created
  pure is whether the function is pure or not
  program is a bytecode representation of the function
  
  body or program can be none, but not at the same time.
  '''
  def __init__(self, argument_names, body, environment, pure = False, program = None):
    self.argument_names = argument_names
    self.body           = body
    self.pure           = pure
    self.environment    = environment
    self.program        = program
    if self.pure:
      raise Exception("unimplemented")

  '''
  This function can be used to prepare for a function call.
  arguments is an array of the parameters
  
  It returns an environment where the parameters have been bounded and a bytecode program.
  '''
  def prepare_call(self, *arguments):
    if(len(self.argument_names) != len(arguments)):
      raise invalid_arguments_exception(len(self.argument_names), len(arguments))
    env = klib.environment.environment(self.environment)
    for arg, name in zip(arguments, self.argument_names):
      env.define_value(name, init_value = arg)
    if not self.program:
      bg = klib.bytecode.generator()
      for s in self.body.statements:
        s.accept(bg)
      self.program = bg.finalise_program()
    return (env, self.program)
