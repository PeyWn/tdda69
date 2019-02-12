from klib.io import stdout

class program:
  '''
  This class hold the instructions for a program or a function.
  '''
  def __init__(self):
    self.instructions = []
  def add_instruction(self, instruction):
    '''
    Convenience function to add an instruction to the program
    '''
    self.instructions.append(instruction)
  def current_index(self):
    '''
    Return the current index, for use in jump instructions, for instnace.
    '''
    return len(self.instructions)
  def print(self, stream = stdout):
    '''
    Print the list of instruction with their index, operands and parameterss
    '''
    for i in range(0, len(self.instructions)):
      inst = self.instructions[i]
      stream.write("{}: {} ({})", i, inst.opcode.name, inst.opcode.index)
      for k in inst.params:
        stream.write(" {}={}", k, inst.params[k])
      stream.writeln("")
