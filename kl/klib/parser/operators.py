class unary_operator:
  Identity        = 0
  AdditiveInverse = 1
  LogicalNegation = 2
  Tilde           = 3
  
class binary_operator:
  Member          = 0
  Subscript       = 1
 
  Assignment      = 5
  Binding         = 6
 
  Addition        = 10
  Substraction    = 11
  Multiplication  = 12
  Division        = 13
  Remainder       = 14
  ShiftLeft       = 15
  ShiftRight      = 16
  
  LogicalAnd      = 20
  LogicalOr       = 21
  
  Equal           = 30
  NotEqual        = 31
  Less            = 32
  Greater         = 33
  LessEqual       = 34
  GreaterEqual    = 35
  
  Precedence      = [Member, Subscript, Multiplication, Division, ShiftLeft, ShiftRight, Remainder, Addition, Substraction, Equal, NotEqual, Less, Greater, LessEqual, GreaterEqual, LogicalAnd, LogicalOr, Assignment, Binding ]
