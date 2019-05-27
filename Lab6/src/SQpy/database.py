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

      elif query.token == token.delete_from:
          q = self.ast_op(query.where, query.table)
          for e in q:
            self.e_list[query.table].remove(e)



  def ast_op(self, node, table_name):
      if node.token == token.op_and:
          res = []
          for e in node.operands:
              res.append(self.ast_op(e, table_name))

          match = res[0]
          for i in range(1, len(res)):
              match = list(set(match).intersection(res[i]))
          return match

      elif node.token == token.op_equal:
          res = []
          for e in self.e_list[table_name]:
              for id in node.operands[0].identifier:
                  if e._asdict()[id] == node.operands[1]:
                      res.append(e)
          return res

      elif node.token == token.op_inferior:
          res = []
          for e in self.e_list[table_name]:
              for id in node.operands[0].identifier:
                  if e._asdict()[id] < node.operands[1]:
                      res.append(e)
          return res

      elif node.token == token.op_superior:
          res = []
          for e in self.e_list[table_name]:
              for id in node.operands[0].identifier:
                  if e._asdict()[id] > node.operands[1]:
                      res.append(e)
          return res

      elif node.token == token.op_divide:
          print('divide inte implementerad')
          pass
