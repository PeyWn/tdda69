import os

import klib.parser
import klib.lexer
import klib.interpreter
import klib.environment
import klib.macro
from klib.io import stdout

class module:
  ''' Represent a kl module '''
  def __init__(self, modules_manager = None):
    self.modules_manager = modules_manager
    self.environment     = None
  def load_file(self, filename, **kargs):
    ''' Load the module from a file (for the arguments, see load_stream function for full list of arguments)'''
    instream = klib.io.stream.input_file_stream(filename)
    self.load_stream(instream, filename=filename, **kargs)
  def load_stream(self, stream, extra_listeners = None, filename = None, developer_verbose = False, include_dirs = []):
    '''
    Load the module from a stream.
    :param filename: is used for display of errors and in traceback
    :param developer_verbose: is set to true for debugging purposes of the tokens tree
    '''
    
    # Lexer and build the tokens tree
    l = klib.lexer.lexer(stream, filename)
    ttb = klib.lexer.tokens_tree_builder(l)
    tt = ttb.build()
    
    # Include part of the tree
    tt.accept(klib.lexer.includer(filename, include_dirs))
    
    # Print token the trees
    if developer_verbose:
      klib.io.stream.stdout.writeln("After inclusion:")
      klib.lexer.print_tokens_tree(tt)
    
    # Load the macros
    macro_engine = klib.macro.engine()
    tt.accept(klib.macro.rule_builder(macro_engine))
    
    # Apply the macros
    tt.accept(macro_engine)
    
    # Transform keyword in their ___ ___ formt
    tt.accept(klib.lexer.keyworder())
    
    # Print token the trees
    if developer_verbose:
      klib.io.stream.stdout.writeln("Before flateing:")
      klib.lexer.print_tokens_tree(tt)

    # Flaten the tree for parsing
    ttf = klib.lexer.tokens_tree_flatener()
    tt.accept(ttf)
    
    if developer_verbose:
      klib.io.stream.stdout.writeln("Flatening:")
      for tk in ttf.tokens_list:
        klib.io.stream.stdout.writeln("{} ({})", tk.text, tk.type)
      
    
    # Parse
    abuilder = klib.parser.ast_builder()
    if(extra_listeners):
      listener = klib.parser.multi_listeners(extra_listeners + [abuilder])
    else:
      listener = abuilder
    p = klib.parser.parser(klib.lexer.tokens_stream(ttf.tokens_list), listener)
    p.parse()
    
    interp = klib.interpreter.substitution_evaluator(self.modules_manager, klib.environment.environment(), developer_verbose = developer_verbose)
    abuilder.ast.accept(interp)
    self.environment = interp.environment
    pass
