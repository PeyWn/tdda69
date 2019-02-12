from .tokens_tree import *
from .token import token
import klib.exception

class tokens_tree_builder:
  '''
  Build a tree of token from a list
  '''
  def __init__(self, lexer):
    self.lexer = lexer
    self.__token_queue    = []

  def __next_token(self):
    if(len(self.__token_queue) == 0):
      self.__current_token = self.lexer.next_token()
    else:
      self.__current_token = self.__token_queue.pop()
    return self.__current_token

  def build(self):
    self.__next_token() # Get a token
    return token_group_node(self.__build_group(token.EndOfStream))

  def __push_token(self, token = None):
    ''' push a token in the queue
    '''
    if(token == None):
      token = self.__current_token
      self.__current_token = None
    self.__token_queue.append(token)
    
  def __report_unexpected(self, token = None):
    ''' report an unexpected token
    '''
    if(token == None):
      token = self.__current_token
    self.__report_error("Unexpected token: '{}' ({})".format(token.text, token.type), token)

  def __report_error(self, text, token = None):
    ''' function that report an error using the parse_error exception
    '''
    if(token == None):
      token = self.__current_token
    raise parse_error(text, token.line, token.column, self.filename)

  def __build_group(self, end_block):
    children = []
    current_children = []
    end_of_statement = -1
    while True:
      end_of_statement -= 1
      if(self.__current_token.type == end_block):
        if len(current_children) > 0:
          children.append(statement_node(current_children))
        return children
      if(self.__current_token.type == token.EndOfStream):
        self.__report
      
      if self.__current_token.type == token.RightArrow:
        current_children.append(token_node(self.__current_token))
        end_of_statement = 1
      elif self.__current_token.type == token.CurlyBraceStart:
        start_token     = self.__current_token
        self.__next_token()
        block_children  = self.__build_group(token.CurlyBraceEnd)
        current_children.append(block_node(start_token, self.__current_token, block_children))
      elif self.__current_token.type == token.ParenthesisStart:
        start_token     = self.__current_token
        self.__next_token()
        block_children  = self.__build_group(token.ParenthesisEnd)
        current_children.append(block_node(start_token, self.__current_token, block_children))
      elif self.__current_token.type == token.BoxBracketStart:
        start_token     = self.__current_token
        self.__next_token()
        block_children  = self.__build_group(token.BoxBracketEnd)
        current_children.append(block_node(start_token, self.__current_token, block_children))
      else:
        current_children.append(token_node(self.__current_token))
      self.__next_token()
      
      if end_of_statement == 0:
        children.append(statement_node(current_children))
        current_children = []

      if self.__current_token.type == token.Semi or self.__current_token.type == token.Comma or (self.__current_token.type == token.TripleDots and current_children[-1].is_block_node() and current_children[-1].children[-1].is_token_node() and current_children[-1].children[-1].token.type == token.Semi):
        if self.__current_token.type == token.TripleDots:
          current_children.append(token_node(self.__current_token))
        children.append(statement_node(current_children))
        current_children = []
        if self.__current_token.type != token.TripleDots:
          children.append(token_node(self.__current_token))
        self.__next_token()
      
