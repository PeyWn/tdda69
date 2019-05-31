from .ast import token, ast
from collections import namedtuple
from statistics import mean

class database(object):
  def __init__(self):
      self.t_list = {}
      self.e_list = {}
      self.from_table = None
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
          self.from_table = query.table
          q = self.ast_op(query.where, self.e_list[query.table])
          for e in q:
            self.e_list[query.table].remove(e)

      elif query.token == token.update:
          q_set = self.ast_op(query.where, self.e_list[query.table])
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
          self.from_table = query.from_table
          if isinstance(query.columns, ast) and query.columns.token == token.star:
              return self.e_list[query.from_table]

          else:

              fields = []
              fn_flag = False
              for e in query.columns:
                  if isinstance(e, str):
                      fields.append(e)
                  else:
                      fields.append(e[1])
                      if e[0].token == (token.fn_count or token.fn_avg):
                          fn_flag = True

              row = namedtuple('row', fields)


              try:
                  entries = self.ast_op(query.where, self.e_list[query.from_table])
              except:
                  entries = self.e_list[query.from_table]

              if fn_flag:
                  res = self.select_by_table(entries, row, query.columns)
              else:
                  res = self.select_by_entry(entries, row, query.columns)

              return res


  def select_by_entry(self, entries, row, columns):
      res = []
      for e in entries:
          values = []
          for f in columns:
              if isinstance(f, str):
                  values.append(e._asdict()[f])
              else:
                  values.append(self.ast_op(f[0], [e]))
          res.append(row._make(values))
      return res

  def select_by_table(self, table, row, columns):
      res = []
      values = []
      for f in columns:
          values.append(self.ast_op(f[0], table))
      res.append(row._make(values))
      return res

  def ast_op(self, node, entry_list):
      if node.token == token.op_and:
          res = []
          for e in node.operands:
              res.append(self.ast_op(e, entry_list))

          match = res[0]
          for i in range(1, len(res)):
              match = list(set(match).intersection(res[i]))
          return match

      elif node.token == token.op_equal:
          res = []
          for e in entry_list:
              for id in node.operands[0].identifier:
                  if e._asdict()[id] == node.operands[1]:
                      res.append(e)
          return res

      elif node.token == token.op_inferior:
          res = []
          for e in entry_list:
              for id in node.operands[0].identifier:
                  if e._asdict()[id] < node.operands[1]:
                      res.append(e)
          return res

      elif node.token == token.op_superior:
          res = []
          for e in entry_list:
              for id in node.operands[0].identifier:
                  if e._asdict()[id] > node.operands[1]:
                      res.append(e)
          return res

      elif node.token == token.op_divide:
          res = []
          oper = self.eval_operands(node, entry_list)
          for i in range(len(oper[0])):
               res.append(oper[0][i]/oper[1][i])

          '''
          for e in entry_list:
              for id in node.operands[0].identifier:
                  print(id)
                  res = e._asdict()[id]/node.operands[1]
          '''
          return res[0]

      elif node.token == token.fn_count:
          res = 0
          for e in entry_list:
              if node.field in e._fields:
                  res += 1
          return res

      elif node.token == token.fn_avg:
          return mean([x._asdict()[node.field] for x in entry_list])

  def eval_operands(self, node, entries):
      l = []
      for o in node.operands:
          if isinstance(o, ast):

              if o.token == token.identifier:
                  if len(o.identifier) == 1:
                      table = self.from_table
                      key = o.identifier[0]
                  else:
                      table = o.identifier[0]
                      key = o.identifier[1]

                  print(self.e_list[table])
                  l.append([e._asdict()[key] for e in self.e_list[table] if e in entries])

          else:
              l.append([o]*len(entries))

      return l
