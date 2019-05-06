from enum import Enum, unique

@unique
class token(Enum):
  identifier    = 0,
  select        = 1,
  create_table  = 2,
  insert_into   = 3,
  delete_from   = 4,
  update        = 5,
  inner_join    = 6,
  star          = 10,
  op_and        = 20,
  op_equal      = 30,
  op_inferior   = 31,
  op_superior   = 32,
  op_divide     = 40,
  fn_count      = 100,
  fn_avg        = 101
  
  
class ast(object):
  def __init__(self, token, **kwargs):
    self.token = token
    for name,value in kwargs.items():
      self.__setattr__(name,value)

  @staticmethod
  def identifier(*ids):
    return ast(token.identifier, identifier=list(ids))
  @staticmethod
  def select(columns, **kwargs):
    return ast(token.select, columns=columns, **kwargs)
  @staticmethod
  def create_table(name, columns):
    return ast(token.create_table, name=name, columns=columns)
  @staticmethod
  def insert_into(table, **kwargs):
    return ast(token.insert_into, table=table, **kwargs)
  @staticmethod
  def delete_from(table, where):
    return ast(token.delete_from, table=table, where=where)
  @staticmethod
  def update(table, set, where):
    return ast(token.update, table=table, set=set, where=where)
  @staticmethod
  def inner_join(table, on):
    return ast(token.inner_join, table=table, on=on)
  @staticmethod
  def op_and(*operands):
    return ast(token.op_and, operands = list(operands))
  @staticmethod
  def op_equal(a, b):
    return ast(token.op_equal, operands = [a,b])
  @staticmethod
  def op_inferior(a, b):
    return ast(token.op_inferior, operands = [a,b])
  @staticmethod
  def op_superior(a, b):
    return ast(token.op_superior, operands = [a,b])
  @staticmethod
  def op_divide(a, b):
    return ast(token.op_divide, operands = [a,b])
  @staticmethod
  def count(field):
    return ast(token.fn_count, field = field)
  @staticmethod
  def avg(field):
    return ast(token.fn_avg, field = field)
  @staticmethod
  def star():
    return ast(token.star)