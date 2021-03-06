import operator

from klib.ast import visitor as ast_visitor
from klib.parser.operators import binary_operator
from klib.parser import binary_operator, unary_operator
from klib.exception import catch_exception, return_exception
import klib.vm
import klib.parser
import klib.ast
import klib.environment
import klib.environment.reference
import klib.environment.utils as ke_utils

from .kl_exception import kl_exception

class substitution_exception(klib.exception):
  def __init__(self, message, metadata):
    super().__init__(message, metadata = metadata)

unary_operator_functions = {
    unary_operator.AdditiveInverse: operator.neg,
    unary_operator.Identity:        lambda a: a,
    unary_operator.LogicalNegation: operator.not_,
    unary_operator.Tilde:           lambda a: ~int(a)
  }

binary_operator_functions = {
    binary_operator.Addition:       operator.add,
    binary_operator.Substraction:   operator.sub,
    binary_operator.Multiplication: operator.mul,
    binary_operator.Division:       operator.truediv,
    binary_operator.Remainder:      operator.mod,
    binary_operator.ShiftLeft:      lambda a, b: int(a) << int(b),
    binary_operator.ShiftRight:     lambda a, b: int(a) >> int(b),
    binary_operator.LogicalAnd:     operator.and_,
    binary_operator.LogicalOr:      operator.or_,
    binary_operator.Equal:          operator.eq,
    binary_operator.NotEqual:       operator.ne,
    binary_operator.Less:           operator.lt,
    binary_operator.Greater:        operator.gt,
    binary_operator.LessEqual:      operator.le,
    binary_operator.GreaterEqual:   operator.ge
  }

class substitution_evaluator(ast_visitor):
  def __init__(self, modules_manager, environment, developer_verbose = False):
    self.environment = environment
    self.modules_manager = modules_manager
    if(not self.modules_manager):
      self.modules_manager = klib.interpreter.modules_manager()
    self.developer_verbose = developer_verbose

  def visit_ast(self, node):
    self.visit_statements(node.statements)

  def visit_value(self, node):
    return node.value

  def visit_identifier(self, node):
    return klib.environment.reference(None, node.identifier)

  def visit_env_expression(self, node):
    return self.environment

  def visit_function_call(self, node):
    raise Exception("substitution_evaluator: unimplemented")

  def visit_native_call(self, node):
    module = klib.native.modules[node.type]
    native_function = module.get(node.name)
    if module:
      native_function = module.get(node.name)
    else:
      raise klib.exception.unknown_native_type(node.type)
    if not native_function:
      raise klib.exception.unknown_native_function(node.type, node.name)
    args = []
    for arg in node.arguments:
      args.append(self.__get_value(arg.accept(self)))
    native_function(*args)

  def __get_value(self, value):
      return value


  def lambda_declaration(self, node):
    return klib.environment.function(node.arguments, node.body, self.environment, **ke_utils.function_modifiers(node))

  def visit_import_statement(self, node):
    raise Exception("substitution_evaluator: unimplemented")

  def visit_return_expression(self, node): 
    raise return_exception(node.return_value.accept(self))

  def visit_named_block(self, node):
    name = node.names[0]
    sub_env = False
    if len(node.names) > 1:
      sub_env = self.environment.get(name).get_value()
      if isinstance(sub_env, klib.environment.environment):
        self.environment = sub_env
      name = node.names[1]

    if (node.type == '___define___'):
       self.environment.define_value(name, node.body.accept(self))
    elif(node.type == '___cell___'):
        if node.body is None:
          self.environment.define_cell(name)
        else:
          self.environment.define_cell(name, node.body.accept(self))

    if sub_env:
      self.environment = sub_env.parent


  def visit_statements(self, statements):
    for statement in statements:
        statement.accept(self)

  def visit_binary_operation(self, node):
    right = node.right.accept(self)
    left = node.left.accept(self)

    if node.op in binary_operator_functions:
      if isinstance(right, klib.environment.reference):
        right = self.environment.get(right.name).get_value()
      if isinstance(left, klib.environment.reference):
        left = self.environment.get(left.name).get_value()
      return binary_operator_functions[node.op](left, right)

    if node.op == binary_operator.Assignment:
    # eval right then set left if left writable
      if isinstance(right, klib.environment.reference):
        right = self.environment.get(right.name).get_value()

      if self.environment.get(left.name).is_writable():
        return self.environment.get(left.name).set_value(right)
      else:
        raise klib.exception("Not a writable assignment")

    elif node.op == binary_operator.Member:
    # eval left then access thorugh environment
      if isinstance(left, klib.environment.reference):
        left = self.environment.get(left.name).get_value()
      return left.get(right.name).get_value()


  def visit_unary_operation(self, node):
    return unary_operator_functions[node.op](node.right.accept(self))

  def visit_clear_expression(self, node):
    for value in node.values:
      value.accept(self)

  def visit_cond_expression(self, node):
    doelse = True
    arg = node.arguments
    el = arg.pop()
    for a in range(0, len(arg), 2):
      if arg[a].accept(self):
        arg[a+1].accept(self)
        doelse = False
        break

    if doelse:
      el.accept(self)

  def visit_catch_expression(self, node):
    try:
      node.block.accept(self)
    except catch_exception as e:
      if not node.catch_cond is None:
        cond = node.catch_cond.accept(self)
        func_return = False
        if isinstance(cond, bool) and cond:
          node.catch_block.accept(self)
        elif isinstance(cond, klib.environment.function): 
          env = self.environment
          self.environment = node.catch_cond.accept(self).prepare_call(e.message)[0]
          try:
            node.catch_cond.accept(self).body.accept(self)
          except return_exception as re:
            func_return = re.message
          self.environment = env

          if func_return:
            node.catch_block.accept(self)
        else:
          raise catch_exception(e)
      else:
        node.catch_block.accept(self)

  def visit_raise_expression(self, node):
    raise catch_exception(node.expression.accept(self))

  def visit_expression_statement(self, node):
    node.expression.accept(self)

  def visit_block_expression(self, node):
    self.environment = klib.environment.environment(self.environment)
    for statement in node.statements:
      statement.accept(self)
    ret = self.environment
    self.environment = self.environment.parent
    return ret

  def visit_group_expression(self, node):
    for statement in node.statements:
      statement.accept(self)

  def visit_call_trace_expression(self, node):
    return [node.metadata]
