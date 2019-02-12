import klib.lexer
import copy

from .rule import multi_variable_node



class engine(klib.lexer.tokens_tree_editor):
  '''
  '''
  def __init__(self):
    super().__init__()
    self.__rules = []
  
  def add_rule(self, rule):
    self.__rules.append(rule)
