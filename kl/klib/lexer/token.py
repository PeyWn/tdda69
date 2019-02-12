class token:
  '''
  Represent a token
  '''
  Invalid                 = -4
  UnterminatedString      = -3
  EndOfStream             = -2
  
  # Identifiers
  Identifier              = 1
  RuleVariable            = 2
  
  # Literals
  String                  = 10
  Number                  = 11
  
  # Special characters
  Comma                   = 20
  Semi                    = 21
  Colon                   = 22
  Dot                     = 23
  TripleDots              = 24
  
  # Delimithers
  CurlyBraceStart         = 30
  CurlyBraceEnd           = 31
  ParenthesisStart        = 32
  ParenthesisEnd          = 33
  BoxBracketStart         = 34
  BoxBracketEnd           = 35
  
  # Operators
  AssignmentOperator      = 50
  
  # Arithmetic Operators
  PlusOperator            = 60
  MinusOperator           = 61
  MultiplicationOperator  = 62
  DivisionOperator        = 63
  RemainderOperator       = 64
  ShiftLeftOperator       = 65
  ShiftRightOperator      = 66
  TildeOperator           = 67
  
  # Logic operators
  AndOperator             = 70
  OrOperator              = 71
  ExclamationOperator     = 72
  
  # Comparison Operators
  EqualEqualOperator      = 80
  DifferentOperator       = 81
  InferiorOperator        = 82
  SuperiorOperator        = 83
  InferiorEqualOperator   = 84
  SuperiorEqualOperator   = 85
  SameOperator            = 86
  NotSameOperator         = 87
  
  # Supplementary Operators
  RightArrow              = 90
  
  def __init__(self, text, type, line, column, filename):
    self.text     = text
    self.type     = type
    self.line     = line
    self.column   = column
    self.filename = filename
