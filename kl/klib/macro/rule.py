import klib.lexer
from klib.lexer.tokens_tree import print_visitor as tokens_tree_print_visitor

class multi_variable_node:
  def __init__(self, token_node, children_node):
    self.token_node     = token_node
    self.variable       = token_node.token.text[1:]
    self.children_node  = children_node

  def accept(self, visitor, *args):
    return visitor.visit_multi_variable_node(self, *args)

class variable_node:
  def __init__(self, token_node):
    self.token_node = token_node
    self.variable   = token_node.token.text[1:]

  def accept(self, visitor, *args):
    return visitor.visit_variable_node(self, *args)

class match_print_visitor(tokens_tree_print_visitor):
  def visit_multi_variable_node(self, node, indent, first, last, stream):
    self._visit_group(node.children_node, "multi_variable({})".format(node.variable), indent, first, last, stream)

  def visit_variable_node(self, node, indent, first, last, stream):
    stream.writeln("{}variable: {}", self._gen_self_indent(indent, first, last), node.variable)

def print_rule_match(node, stream = klib.io.stdout, indent = ""):
  node.accept(match_print_visitor(), indent, True, True, stream)

class rule:
  '''
  Represent a macro rule, with its match and production rules
  '''
  def __init__(self, match, production):
    self.__match      = match
    self.__production = production
  
  def get_match(self):
    return self.__match
  
  def get_production(self):
    return self.__production
  
  def print(self, stream = klib.io.stdout):
    stream.writeln("Rule ──────────────");
    stream.writeln("───────────── match");
    for c in self.__match:
      stream.write("  ")
      print_rule_match(c, stream, "  ")
    stream.writeln("──────── production");
    stream.write("  ")
    print_rule_match(self.__production, stream, "  ")
