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
      res = []
      for e in self.e_list[name]:
          res.append(e)
      return res


  def execute(self, query):
      if query.token == token.create_table :
          self.t_list[query.name] = namedtuple(query.name, query.columns)
          self.e_list[query.name] = []

      elif query.token == token.insert_into :
          table = self.t_list[query.table]
          table.__new__.__defaults__ = (None,) * len(table._fields)

          try:
              entry = table._make(query.values)
          except:
              entry = table()
              for i in range(len(query.columns)):

                  entry = entry._replace(**{query.columns[i]:query.values[i]})

          self.e_list[query.table].append(entry)
