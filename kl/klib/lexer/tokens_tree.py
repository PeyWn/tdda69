from klib.io import stdout

'''
Class in this module are used to represent a program as a tokens tree
'''

class token_node_base:
  def is_group_node(self):
    return False

  def is_statement_node(self):
    return False
  
  def is_block_node(self):
    return False
  
  def is_token_node(self):
    return False

class token_group_node(token_node_base):
  '''
  Represent a group of tokens.
  '''
  def __init__(self, children):
    self.children = children

  def accept(self, visitor, *args):
    return visitor.visit_token_group_node(self, *args)

  def is_group_node(self):
    return True

class statement_node(token_group_node):
  '''
  Represent a single statement
  '''
  def __init__(self, children):
    super().__init__(children)

  def accept(self, visitor, *args):
    return visitor.visit_statement_node(self, *args)

  def is_statement_node(self):
    return True

class block_node(token_group_node):
  '''
  Represent a block
  '''
  def __init__(self, start_token, end_token, children):
    super().__init__(children)
    self.start_token = start_token
    self.end_token   = end_token

  def accept(self, visitor, *args):
    return visitor.visit_block_node(self, *args)

  def is_block_node(self):
    return True

class token_node(token_node_base):
  '''
  Represent a single token
  '''
  def __init__(self, token):
    self.token = token

  def accept(self, visitor, *args):
    return visitor.visit_token_node(self, *args)

  def is_token_node(self):
    return True

class visitor:
  '''
  Visit the node in the tree
  '''
  def __init__(self):
    pass

  def visit_token_group_node(self, node, *args):
    for c in node.children:
      c.accept(self, *args)
  
  def visit_statement_node(self, node, *args):
    self.visit_token_group_node(node, *args)
  
  def visit_block_node(self, node, *args):
    self.visit_token_group_node(node, *args)
  
  def visit_token_node(self, node, *args):
    pass

class editor:
  '''
  Visitor that can be used to transform a token tree
  '''
  def __init__(self):
    pass

  def edit_children(self, children, *args):
    newc = []
    for c in children:
      nc = c.accept(self, *args)
      if nc:
        try:
          newc += nc
        except TypeError:
          newc.append(nc)
    return newc

  def visit_token_group_node(self, node, *args):
    node.children = self.edit_children(node.children, *args)
    return node
  
  def visit_statement_node(self, node, *args):
    return self.visit_token_group_node(node, *args)
  
  def visit_block_node(self, node, *args):
    return self.visit_token_group_node(node, *args)
  
  def visit_token_node(self, node, *args):
    return node

class print_visitor(visitor):
  '''
  visitor used to print to the output the content of a tree
  '''
  def __init__(self):
    pass


  def _gen_self_indent(self, indent, first, last):
    if(last):
      if first:
        return "─"
      else:
        return indent + "└"
    elif first:
      return "┬"
    else:
      return indent + "├"
  
  def _visit_group(self, node, name, indent, first, last, stream):
    stream.write("{}{}", self._gen_self_indent(indent, first, last), name)
    if(last):
      indent += " "
    else:
      indent += "│"
    indent += " " * len(name)
    if len(node.children) > 0:
      for i in range(0, len(node.children)):
        node.children[i].accept(self, indent, i == 0, i == len(node.children) - 1, stream)
    else:
      stream.writeln("")
    
  
  def visit_token_group_node(self, node, indent, first, last, stream):
    self._visit_group(node, "group", indent, first, last, stream)
    
  def visit_statement_node(self, node, indent, first, last, stream):
    self._visit_group(node, "statement", indent, first, last, stream)
    
    
  def visit_block_node(self, node, indent, first, last, stream):
    self._visit_group(node, "block{}{}".format(node.start_token.text, node.end_token.text), indent, first, last, stream)
    
    
  def visit_token_node(self, node, indent, first, last, stream):
    stream.writeln("{}token: {} ({})", self._gen_self_indent(indent, first, last), node.token.text, node.token.type)

def print_tokens_tree(node, stream = stdout, indent = ""):
  node.accept(print_visitor(), indent, True, True, stream)
  
class flatener(visitor):
  '''
  Transform a tree of tokens to a list of tokens.
  '''
  def __init__(self):
    super().__init__()
    self.tokens_list = []

  def visit_block_node(self, node):
    self.tokens_list.append(node.start_token)
    super().visit_block_node(node)
    self.tokens_list.append(node.end_token)
  
  def visit_token_node(self, node):
    self.tokens_list.append(node.token)
