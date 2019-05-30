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

      elif query.token == token.update:
          q_set = self.ast_op(query.where, query.table)
          for e in q_set:
              index, entry = 0, None
              for i, x in enumerate(self.e_list[query.table]):
                  if x == e:
                      index = i
                      entry = e
                      break;

              for s in query.set:
                  entry = entry._replace(**{s[0]:s[1]})
              self.e_list[query.table][i] = entry

      elif query.token == token.select:
          if isinstance(query.columns, ast) and query.columns.token == token.star:
              return self.e_list[query.from_table]

          else:

              fields = []
              for e in query.columns:
                  if isinstance(e, str):
                      fields.append(e)
                  else:
                      fields.append(e[1])

              row = namedtuple('row', fields)


              res = []
              try:
                  entries = self.ast_op(query.where, query.from_table)
              except:
                  entries = self.e_list[query.from_table]

              for e in entries:
                  values = []
                  for f in query.columns:
                      if isinstance(f, str):
                          values.append(e._asdict()[f])
                      else:
                        if f[0].token == token.op_divide:
                            for id in f[0].operands[0].identifier:
                                value = e._asdict()[id]/f[0].operands[1]
                                values.append(value)

                  res.append(row._make(values))
              return res






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
