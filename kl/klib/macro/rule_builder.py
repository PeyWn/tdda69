import klib.lexer
from klib.exception import parse_error
from .rule import variable_node, multi_variable_node, rule

class rule_match_builder(klib.lexer.tokens_tree_editor):
  def __init__(self):
    pass
  
  def __is_multi_variable(self, index, c, children):
    if c.is_token_node() and c.token.type == klib.lexer.token.RuleVariable and index + 2 < len(children):
      c2 = children[index + 2]
      return c2.is_token_node() and c2.token.type == klib.lexer.token.TripleDots
    return False
  
  def edit_children(self, children, *args):
    newc = []
    i = 0
    while i < len(children):
      c  = children[i]
      
      if self.__is_multi_variable(i, c, children):
        newc.append(multi_variable_node(c, children[i+1].accept(self)))
        i += 3
      else:
        nc = c.accept(self, *args)
        if nc:
          try:
            newc[:] = nc
          except TypeError:
            newc.append(nc)
        i += 1
    return newc

  def visit_statement_node(self, node):
    node = super().visit_statement_node(node)
    if len(node.children) == 1 and type(node.children[0]) in [variable_node, multi_variable_node]:
      return node.children[0]
    else:
      return node
  
  def visit_token_node(self, node):
    if node.token.type == klib.lexer.token.RuleVariable:
      return variable_node(node)
    else:
      return node

class rule_builder(klib.lexer.tokens_tree_editor):
  def __init__(self, macro_engine):
    self.macro_engine = macro_engine
  def visit_token_group_node(self, node):
    if len(node.children) > 1 and hasattr(node.children[0], "token") and (node.children[0].token.text == "___rule___" or node.children[0].token.text == "rule"):
      rule_token = node.children[0].token
      arrow_index = len(node.children) - 2
      arrow_node = node.children[arrow_index]
      if not hasattr(arrow_node, "token") or arrow_node.token.type != klib.lexer.token.RightArrow:
        raise parse_error("Missing right arrow or too many production", rule_token.line, rule_token.column, rule_token.filename)
      if(arrow_index == 1):
        raise parse_error("Empty rule is not allowed", rule_token.line, rule_token.column, rule_token.filename)
      
      match_tokens = rule_match_builder().edit_children(node.children[1:arrow_index])
      production_tokens = node.children[arrow_index+1].accept(rule_match_builder())
      
      r = rule(match_tokens, production_tokens)
      self.macro_engine.add_rule(r)
      return None
    return super().visit_token_group_node(node)
