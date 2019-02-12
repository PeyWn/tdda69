from klib.lexer import token
from .tokens_tree import visitor

class keyworder(visitor):
  ''' keyworder is a token_stream modifier which convert
      keywords from their user friendly form to their
      immutable form (aka "keyword" to "___keyword___")
  '''
  def __init__(self):
    super().__init__()
    self.identifier_map = {
        "cell":       "___cell___",
        "catch":      "___catch___",
        "clear":      "___clear___",
        "cond":       "___cond___",
        "define":     "___define___",
        "env":        "___env___",
        "false":      "___false___",
        "function":   "___function___",
        "import":     "___import___",
        "procedure":  "___procedure___",
        "raise":      "___raise___",
        "return":     "___return___",
        "rule":       "___rule___",
        "true":       "___true___"
      }
  
  def visit_token_node(self, node):
    tok = node.token
    if(tok.type == token.Identifier):
      tok.text = self.identifier_map.get(tok.text, tok.text)
