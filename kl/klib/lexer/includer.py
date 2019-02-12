import os
import klib.io

from .token import token
from .tokens_tree import visitor
from .lexer import lexer
from .tokens_tree_builder import tokens_tree_builder

class includer(visitor):
  ''' includer is a token_stream modifier which check for
      ___include___ and then include the file in the tree
  '''
  def __init__(self, filename, include_dirs):
    super().__init__()
    self.filename = filename
    self.include_dirs = include_dirs
    
  def visit_token_group_node(self, node):
    last = len(node.children)
    i = 0
    while i < last:
      child = node.children[i]
      if(hasattr(child, 'children') and len(child.children) == 2 and hasattr(child.children[0], 'token') and child.children[0].token.text == "___include___"):
        if(child.children[1].start_token and child.children[1].start_token.type == token.ParenthesisStart and child.children[1].end_token.type == token.ParenthesisEnd):
          arguments = child.children[1].children
          if(len(arguments) == 1):
            filename = arguments[0].children[0].token.text
            base_filename = filename
            
            if not os.path.isabs(filename) and arguments[0].children[0].token.filename:
              filename = os.path.join(os.path.dirname(self.filename), base_filename)
            
            if not os.path.exists(filename):
              for p in self.include_dirs:
                filename = os.path.join(p, base_filename)
                if os.path.exists(filename):
                  break
            
            instream = klib.io.stream.input_file_stream(filename)
            
            l = lexer(instream, filename)
            ttb = tokens_tree_builder(l)
            tt = ttb.build()
            
            if len(node.children) > i+1 and hasattr(node.children[i+1], 'token') and node.children[i+1].token.type == token.Semi:
              del node.children[i+1]
              last -= 1
            del node.children[i]
            node.children[i:i] = tt.children
            i -= 1
      i += 1
            

    super().visit_token_group_node(node)
