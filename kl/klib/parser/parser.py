import re

import klib.exception
from klib.lexer import token
from klib.parser.operators import unary_operator, binary_operator
import os.path

from .metadata import metadata

class parse_error(klib.exception):
  def __init__(self, message, line, column, filename):
    super().__init__("")
    self.message = message # cannot pass message to super constructor as that fails when report an error with token '}'
    self.line     = line
    self.column   = column
    self.filename = filename

class parser:
  ''' Read tokens from token_stream and emit statements in the listener
  '''
  def __init__(self, token_stream, listener, parent_metadata = None):
    self.token_stream     = token_stream
    self.listener         = listener
    self.parent_metadata  = parent_metadata
    self.block_name_stack = []
    self.__token_queue    = []
    self.__unary_operators  = { token.PlusOperator: unary_operator.Identity,
                                token.MinusOperator: unary_operator.AdditiveInverse,
                                token.ExclamationOperator: unary_operator.LogicalNegation,
                                token.TildeOperator: unary_operator.Tilde }
    self.__binary_operators = { token.PlusOperator: binary_operator.Addition,
                                token.MinusOperator: binary_operator.Substraction,
                                token.DivisionOperator: binary_operator.Division,
                                token.MultiplicationOperator: binary_operator.Multiplication,
                                token.RemainderOperator: binary_operator.Remainder,
                                token.EqualEqualOperator: binary_operator.Equal,
                                token.DifferentOperator: binary_operator.NotEqual,
                                token.SuperiorOperator: binary_operator.Greater,
                                token.SuperiorEqualOperator: binary_operator.GreaterEqual,
                                token.InferiorOperator: binary_operator.Less,
                                token.InferiorEqualOperator: binary_operator.LessEqual,
                                token.AssignmentOperator: binary_operator.Assignment,
                                token.Colon: binary_operator.Binding,
                                token.Dot: binary_operator.Member,
                                token.ShiftLeftOperator: binary_operator.ShiftLeft,
                                token.ShiftRightOperator: binary_operator.ShiftRight,
                                token.AndOperator: binary_operator.LogicalAnd,
                                token.OrOperator: binary_operator.LogicalOr
                                }
  ''' entry point in the parser.
  '''
  def parse(self):
    self.__next_token() # Get a token
    self.__parse_block(token.EndOfStream, True)
  def __metadata(self, token):
    if len(self.block_name_stack) == 0:
      block_name = "___main___"
    else:
      block_name = self.block_name_stack[-1]
    return metadata(token.line, token.column, token.filename, block_name, self.parent_metadata)
  def __send(self, func, *args, metadata = None):
    if metadata == None:
      metadata = self.__metadata(self.__current_token)
    func(*args, metadata)
  ''' get the next token and store it in self.__current_token
  '''
  def __next_token(self):
    if(len(self.__token_queue) == 0):
      self.__current_token = self.token_stream.next_token()
    else:
      self.__current_token = self.__token_queue.pop()
    return self.__current_token
  
  def __is_current_token(self, type):
    if self.__current_token.type != type:
      self.__report_unexpected()
  
  def __is_next_token(self, type):
    if self.__next_token().type != type:
      self.__report_unexpected()
  def __is_next_token_types(self, types):
    if not(self.__next_token().type in types):
      self.__report_unexpected()
  ''' push a token in the queue
  '''
  def __push_token(self, token = None):
    if(token == None):
      token = self.__current_token
      self.__current_token = None
    self.__token_queue.append(token)
    
  ''' report an unexpected token
  '''
  def __report_unexpected(self, token = None):
    if(token == None):
      token = self.__current_token
    self.__report_error("Unexpected token: '{}' ({})".format(token.text, token.type), token)
  ''' function that report an error using the parse_error exception
  '''
  def __report_error(self, text, token = None):
    if(token == None):
      token = self.__current_token
    raise parse_error(text, token.line, token.column, token.filename)
  ''' check if an identifier is a valid variable identifier
  '''
  def __check_valid_identifier(self, token = None):
    if(token == None):
      token = self.__current_token
    left_non_underscore = 0
    while left_non_underscore < len(token.text):
      if token.text[left_non_underscore] != '_':
        break
      left_non_underscore += 1
    right_non_underscore = len(token.text) - 1
    while right_non_underscore >= 0:
      if token.text[right_non_underscore] != '_':
        break
      right_non_underscore -= 1
    right_non_underscore = len(token.text) - right_non_underscore - 1
    if left_non_underscore >= 3 and right_non_underscore >= 3:
       self.__report_error("Invalid identifier: '{}'".format(token.text), token)
    
  ''' function that parse a kl block
  '''
  def __parse_block(self, end_block, top_block):
    #raise error_message("Not implemented", 0, 0)
    #return None
    while(self.__current_token.type != token.EndOfStream):
      if(self.__current_token.type == end_block):
        self.__next_token()
        return
      elif(self.__current_token.type == token.Identifier):
        start_token = self.__current_token
        # Check if we have a named block
        if(start_token.type == token.Identifier):
          if(self.__next_token().type == token.Identifier):
            block_type = start_token.text
            self.__check_valid_identifier()
            
            # Get block list of names
            block_names = [self.__current_token.text]
            self.__next_token()
            while self.__current_token.type == token.Dot:
              self.__is_next_token(token.Identifier)
              block_names.append(self.__current_token.text)
              self.__next_token()
            
            # Treat ___import___ seperately
            if block_type == "___import___":
              # Parse version number
              self.__is_current_token(token.Number)
              # Extract minor/major number
              m = re.search('(\d+).(\d+)', str(self.__current_token.text))
              if m:
                major = int(m.group(1))
                minor = int(m.group(2))
              else:
                m = re.search('\d+', str(self.__current_token.text))
                if(m):
                  major = int(m.group(0))
                  minor = 0
                else:
                  self.__report_error("Invalid version {}".format(self.__current_token.text))
              # Emit import_statement
              self.__send(self.listener.import_statement, block_names, major, minor)
              self.__is_next_token(token.Semi)
              self.__next_token() # Skip ';'
            else:
              # Check for block arguments
              self.block_name_stack.append(".".join(block_names))
              (arguments, modifiers, op) = self.__parse_function_definition()
              if self.__current_token.type != token.Semi:
                self.__parse_single_expression()
                if self.__is_binary_operator():
                  self.__parse_flat_binary_operator([token.Semi])
              self.__send(self.listener.named_block, block_type, block_names, arguments, modifiers, op)
              if self.__current_token.type == token.Semi:
                self.__next_token() # Skip ';'
              self.block_name_stack.pop()
          else: # Then we have an expression
            self.__push_token()
            self.__current_token = start_token
            self.__parse_expression_statement()
        else:
          self.__report_unexpected()
      elif self.__current_token.type in [token.CurlyBraceStart, token.ParenthesisStart, token.BoxBracketStart]:
        self.__parse_expression_statement()
      else:
        self.__report_unexpected()
  
  def __parse_function_definition(self):
    arguments = []
    if(self.__current_token.type == token.ParenthesisStart):
      while(self.__next_token().type != token.ParenthesisEnd):
        if(self.__current_token.type == token.Identifier):
          self.__check_valid_identifier()
          arguments.append(self.__current_token.text)
        if(self.__next_token().type == token.ParenthesisEnd):
          break
        elif(self.__current_token.type == token.Comma):
          pass
        else:
          self.__report_unexpected()
    else:
      self.__push_token()
    modifiers = []
    while(self.__is_next_token_types([token.CurlyBraceStart, token.AssignmentOperator, token.Colon, token.Semi])):
      if(self.__current_token.type == token.Identifier):
        modifiers.append(self.__current_token.text)
      else:
        self.__report_unexpected()
    op = binary_operator.Assignment
    if(self.__current_token.type == token.Colon):
      op = binary_operator.Binding
      self.__next_token()
    elif(self.__current_token.type == token.AssignmentOperator):
      self.__next_token()
    return (arguments, modifiers, op)
  
  def __parse_expression_statement(self):
    self.__send(self.listener.start_expression)
    self.__parse_expression()
    self.__send(self.listener.end_expression)
    if(self.__current_token.type == token.Semi):
      self.__next_token()
    
  def __parse_expression(self, termination = [token.Semi, token.CurlyBraceEnd]):
    self.__parse_single_expression()
    if self.__current_token.type in termination:
      return
    elif self.__current_token.type == token.ParenthesisStart:
      m = self.__metadata(self.__current_token)
      self.__send(self.listener.function_call_expression, self.__parse_call(), metadata = m)
    elif self.__is_binary_operator():
      self.__parse_flat_binary_operator(termination)
    else:
      self.__report_unexpected()
  
  def __parse_single_expression(self):
    if self.__current_token.type == token.ParenthesisStart:
      self.__next_token() # Skip '('
      self.__parse_expression([token.ParenthesisEnd])
      self.__is_current_token(token.ParenthesisEnd)
      self.__next_token() # Skip ')'
    elif self.__is_unary_operator():
      unop = self.__unary_operators[self.__current_token.type]
      self.__next_token()
      self.__parse_single_expression()
      self.__send(self.listener.unary_expression, unop)
    elif(self.__current_token.type == token.Identifier):
      if(self.__current_token.text == "___true___"):
        self.__send(self.listener.value_expression, True)
        self.__next_token() # skip the value
      elif(self.__current_token.text == "___false___"):
        self.__send(self.listener.value_expression, False)
        self.__next_token() # skip the value
      elif(self.__current_token.text == "___native_call___"):
        m = self.__metadata(self.__current_token)
        self.__next_token()
        self.__send(self.listener.native_call_expression, self.__parse_call() - 2, metadata = m)
      elif(self.__current_token.text == "___cond___"):
        m = self.__metadata(self.__current_token)
        self.__next_token()
        self.__send(self.listener.cond_expression, self.__parse_call(), metadata = m)
      elif(self.__current_token.text == "___clear___"):
        m = self.__metadata(self.__current_token)
        self.__next_token()
        self.__send(self.listener.clear_expression, self.__parse_call(), metadata = m)
      elif(self.__current_token.text == "___return___"):
        m = self.__metadata(self.__current_token)
        self.__next_token()
        v = self.__parse_call()
        if v == 0 or v==1:
          self.__send(self.listener.return_expression, v, metadata = m)
        else:
          self.__report_error("Invalid number of arguments in return call.", token = c)
      elif(self.__current_token.text == "___catch___"):
        c = self.__current_token
        m = self.__metadata(self.__current_token)
        self.__next_token()
        args = self.__parse_call()
        if(args != 2 and args != 3):
          self.__report_error("Wrong number of arguments in cond call.", token = c)
        
        self.__send(self.listener.catch_expression, args, metadata = m)
      elif(self.__current_token.text == "___raise___"):
        c = self.__current_token
        m = self.__metadata(self.__current_token)
        self.__next_token()
        if(self.__parse_call() != 1):
          self.__report_error("Wrong number of arguments in raise call.", token = c)
        
        self.__send(self.listener.raise_expression, metadata = m)
        
      elif(self.__current_token.text == "___function___"):
        # ___Function___ means lambda
        self.__next_token()
        (arguments, modifiers, op) = self.__parse_function_definition()
        if(op != binary_operator.Assignment):
          raise Exception("Internal error: lambda can only be assigned, not binded")
        self.__is_current_token(token.CurlyBraceStart)
        self.__next_token()
        self.__send(self.listener.start_block_expression)
        self.__parse_block(token.CurlyBraceEnd, False)
        self.__send(self.listener.end_block_expression)
        self.__send(self.listener.lambda_declaration_expression, arguments, modifiers)
      elif(self.__current_token.text == "___env___"):
        self.__next_token() # Skip '___env___'
        self.__send(self.listener.env_expression)
      elif(self.__current_token.text == "___calltrace___"):
        self.__next_token() # Skip '___calltrace___'
        self.__send(self.listener.call_trace_expression)
      else:
        # Anything else is accessing a variable
        self.__send(self.listener.identifier_expression, self.__current_token.text)
        self.__next_token() # skip the identifer
    elif(self.__current_token.type == token.Number or self.__current_token.type == token.String):
      self.__send(self.listener.value_expression, self.__current_token.text)
      self.__next_token() # skip the value
    elif(self.__current_token.type == token.CurlyBraceStart):
      self.__send(self.listener.start_block_expression)
      self.__next_token() # Skip '{'
      self.__parse_block(token.CurlyBraceEnd, False)
      self.__send(self.listener.end_block_expression)
    elif(self.__current_token.type == token.BoxBracketStart):
      self.__send(self.listener.start_group_expression)
      self.__next_token() # Skip '['
      self.__parse_block(token.BoxBracketEnd, False)
      self.__send(self.listener.end_group_expression)
    else:
      self.__report_unexpected()
    
  def __parse_flat_binary_operator(self, termination):
    while self.__is_binary_operator():
      self.__parse_binary_operator(termination)
  
  def __parse_binary_operator(self, termination):
    binop = self.__binary_operators.get(self.__current_token.type)
    self.__next_token()
    self.__parse_single_expression()
    
    # Parse function call
    if self.__current_token.type == token.ParenthesisStart:
      if(binop == binary_operator.Member):
        self.__send(self.listener.binary_expression, binop)
        
      while self.__current_token.type == token.ParenthesisStart:
        # function call
        if self.__current_token.type == token.ParenthesisStart:
          m = self.__metadata(self.__current_token)
          self.__send(self.listener.function_call_expression, self.__parse_call(), metadata = m)
        else:
          self.__report_error("Unimplemented")

      if(binop == binary_operator.Member):
        return
    if(self.__current_token.type in termination):
      self.__send(self.listener.binary_expression, binop)
    elif(self.__is_binary_operator()):
      next_binop = self.__binary_operators.get(self.__current_token.type)
      if binary_operator.Precedence.index(next_binop) < binary_operator.Precedence.index(binop):
        self.__parse_binary_operator(termination)
      self.__send(self.listener.binary_expression, binop)
    else:
      self.__report_unexpected()
      
  def __parse_call(self):
    self.__is_current_token(token.ParenthesisStart)
    self.__next_token() # Skip '('
    arguments = 0
    while self.__current_token.type != token.EndOfStream and self.__current_token.type != token.ParenthesisEnd:
      arguments += 1
      self.__parse_expression([token.Comma, token.ParenthesisEnd])
      
      if self.__current_token.type == token.Comma:
        self.__next_token()
    self.__next_token()
    return arguments
  
  def __is_unary_operator(self, tok = None):
    if(tok == None):
      tok = self.__current_token
    return tok.type in self.__unary_operators

  def __is_binary_operator(self, tok = None):
    if(tok == None):
      tok = self.__current_token
    return tok.type in self.__binary_operators
