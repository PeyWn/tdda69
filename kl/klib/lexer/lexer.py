from .token import token

class lexer:
  '''
  lexer for kl, takes a stream as argument and a filename used as metadata for the tokens
  '''
  def __init__(self, stream, filename):
    self.stream = stream
    self.filename = filename
    self.line_number = 1
    self.column_number = 0
    self.current_char = None
    self.current_char_is_space = False
    self.special_token = { ',': token.Comma, '.': token.Dot, ';': token.Semi, ':': token.Colon,
                           '...': token.TripleDots,
                           '{': token.CurlyBraceStart, '}': token.CurlyBraceEnd,
                           '(': token.ParenthesisStart, ')': token.ParenthesisEnd,
                           '[': token.BoxBracketStart, ']': token.BoxBracketEnd,
                           '+': token.PlusOperator, '-': token.MinusOperator,
                           '<<': token.ShiftLeftOperator, '>>': token.ShiftRightOperator,
                           '%': token.RemainderOperator,
                           '*': token.MultiplicationOperator, '/': token.DivisionOperator,
                           '=': token.AssignmentOperator, '==': token.EqualEqualOperator,
                           '=>': token.RightArrow,
                           '!=': token.DifferentOperator,
                           '<': token.InferiorOperator, '<=': token.InferiorEqualOperator,
                           '>': token.SuperiorOperator, '>=': token.SuperiorEqualOperator,
                           '!': token.ExclamationOperator, '~': token.TildeOperator,
                           '&&': token.AndOperator, '||': token.OrOperator }
  
  def __get_next_char(self):
    c = self.stream.next_char()
    if c == None:
      return c
    if c == '\n':
      self.line_number += 1
      self.column_number = 0
    else:
      self.column_number += 1
    self.current_char = c
    self.current_char_is_space = c.isspace()
    return self.current_char
  def __unget_char(self, c, column):
    if(c == '\n'):
      self.line_number -= 1
    self.column_number = column
    self.stream.unget_char(c)
  def __get_next_non_seperator_char(self):
    while(self.__get_next_char() != None):
      if(not self.current_char_is_space):
        return self.current_char
    return None
  def __get_identifier(self, type):
    token_line   = self.line_number
    token_column = self.column_number
    last_column  = token_column
    text = self.current_char
    
    while(self.__get_next_char() != None):
      if(self.current_char.isalpha() or self.current_char.isdigit() or self.current_char == '_'):
        text += self.current_char
      else:
        self.__unget_char(self.current_char, last_column)
        return token(text, type, token_line, token_column, self.filename)
      last_column = self.column_number
    return token(text, type, token_line, token_column, self.filename)
  def __get_number(self):
    token_line   = self.line_number
    token_column = self.column_number
    last_column  = token_column
    text = self.current_char
    rightAfterExponent = False
    while(self.__get_next_char() != None):
      if(self.current_char == '.' or self.current_char == 'e' or self.current_char.isdigit()):
        text += self.current_char
        if(self.current_char == 'e'):
          rightAfterExponent = True
        else:
          rightAfterExponent = False
      elif(self.current_char == '-' and rightAfterExponent):
        text += self.current_char
        rightAfterExponent = False
      else:
        self.__unget_char(self.current_char, token_column)
        return token(float(text), token.Number, token_line, token_column, self.filename)
      last_column = self.column_number
    return token(float(text), token.Number, token_line, token_column, self.filename)
  def __get_string(self, termination):
    token_line   = self.line_number
    token_column = self.column_number
    text = ""
    while(self.__get_next_char() != None):
      if(self.current_char == termination):
        return token(text, token.String, token_line, token_column, self.filename)
      text += self.current_char
    return token(text, token.UnterminatedString, token_line, token_column, self.filename)

  def __safe_cat(self, *args):
    i = 0
    while(i < len(args)):
      if args[i] != None:
        res = args[i]
        break
      i += 1
    i += 1
    while(i < len(args)):
      if args[i] != None:
        res += args[i]
      i += 1
    return res

  def next_token(self):
    if(self.__get_next_non_seperator_char() == None):
      return token(None, token.EndOfStream, self.line_number, self.column_number, self.filename)
    token_line   = self.line_number
    token_column = self.column_number
    
    if(self.current_char == '#'):
      while(self.__get_next_char() != None):
        if(self.current_char == '\n'):
          break
      return self.next_token()

    elif(self.current_char.isalpha() or self.current_char == '_'):
      return self.__get_identifier(token.Identifier)
    elif(self.current_char == '$'):
      return self.__get_identifier(token.RuleVariable)
    elif(self.current_char.isdigit()):
      return self.__get_number()
    elif(self.current_char == '"' or self.current_char == "'"):
      return self.__get_string(self.current_char)
    else:
      c1 = self.current_char
      c2 = self.__get_next_char()
      c2_column_number = self.column_number
      c3 = self.__get_next_char()
      c = self.__safe_cat(c1, c2, c3)
      t = self.special_token.get(c, token.Invalid)
      if(t == token.Invalid):
        self.__unget_char(c3, c2_column_number)
        c = self.__safe_cat(c1, c2)
        t = self.special_token.get(c, token.Invalid)
        if(t == token.Invalid):
          self.__unget_char(c2, token_column)
          c = c1
          t = self.special_token.get(c, token.Invalid)
      if t != token.Invalid:
        return token(c, t, token_line, token_column, self.filename)
      else:
        return token(c1, token.Invalid, token_line, token_column, self.filename)

    return token(self.current_char, token.Invalid, token_line, token_column, self.filename)
