from .token import token

class tokens_stream:
  '''
  Take a list of tokens and stream them through the next_token interface
  '''
  def __init__(self, tokens_list):
    self.tokens_list = tokens_list
    self.previous_index = -1
  
  def next_token(self):
    self.previous_index += 1
    if self.previous_index < len(self.tokens_list):
      return self.tokens_list[self.previous_index]
    else:
      tok = self.tokens_list[-1]
      return token(None, token.EndOfStream, tok.line, tok.column + 1, tok.filename)
      
