from .ast import token, ast
from collections import namedtuple

class database(object):
  def __init__(self):
      self.t_list = {}
      self.e_list = {}
  def tables(self):
      return [ e for e in self.t_list.keys()]

  def fields(self, name):
      f = self.t_list[name]
      return list(f._fields)

  def dump_table(self, name):
      pass
  def execute(self, query):
      if query.token == token.create_table :
          self.t_list[query.name] = namedtuple(query.name, query.columns)
      elif query.token == token.insert_into :
          table = self.t_list[query.table]
          entry = table._make(query.values)
