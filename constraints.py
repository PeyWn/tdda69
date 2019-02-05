""" SICP Constraint system, Python version.

Translated from R6RS Scheme in 2015."""

# Connectors
class ConnectorError(Exception):
  def __init__(self, name, old, new):
    self.origin = name
    self.old_val = old
    self.new_val = new

  def __str__(self):
    return self.origin + ": " + repr(self.old_val) + " is not " + repr(self.new_val)

class Connector:
  def __init__(self, name_ = "noname"):
    self.value  = None
    self.setter = None
    self.name   = name_
    self.constraints = []
    self.show_updates = False

  def has_value(self):
    return self.setter is not None

  def set_value(self, new_val, new_setter):
    if not self.has_value():
      if self.show_updates:
        print("SET:", self.name, "=", new_val)
      self.value = new_val
      self.setter = new_setter
      self.__for_each_but(new_setter, lambda constraint: constraint.process(), self.constraints)
    elif not self.value == new_val:
      raise ConnectorError(self.name, self.value, new_val)

  def forget(self, retractor):
    if retractor == self.setter:
      if self.show_updates:
        print("FORGET: ", self.name)
      self.setter = None
      self.value = None
      self.__for_each_but(retractor, lambda constraint: constraint.forget(), self.constraints)

  def connect(self, new_constraint):
    if new_constraint not in self.constraints:
      self.constraints.append(new_constraint)
    if self.has_value():
      new_constraint.process()
    return "done"

  def __for_each_but(self,to_skip, f, seq):
    for e in seq:
      if not e == to_skip: f(e)

class Constant:
  def __init__(self, value, connector):
    self.value = value
    connector.connect(self)
    connector.set_value(value, self)

class Adder:
  def __init__(self, a1, a2, sum):
    self.a1 = a1
    self.a2 = a2
    self.sum = sum
    a1.connect(self)
    a2.connect(self)
    sum.connect(self)

  def process(self):
    a1, a2, sum = self.a1, self.a2, self.sum

    if a1.has_value() and self.a2.has_value():
      sum.set_value(a1.value + a2.value, self)
    elif a1.has_value() and sum.has_value():
      a2.set_value(self.sum.value - a1.value, self)
    elif a2.has_value() and sum.has_value():
      a1.set_value(sum.value - a2.value, self)

  def forget(self):
    self.sum.forget(self)
    self.a1.forget(self)
    self.a2.forget(self)

class Multiplier:
  def __init__(self, m1_, m2_, prod_, name_ = "anonymous multiplier"):
    self.m1 = m1_
    self.m2 = m2_
    self.prod = prod_
    self.name = name_
    m1_.connect(self)
    m2_.connect(self)
    prod_.connect(self)

  def process(self):
    m1, m2, prod = self.m1, self.m2, self.prod

    if m1.has_value() and m1.value == 0 or \
       m2.has_value() and m2.value == 0:
      prod.set_value(0, self)
    elif m1.has_value() and m2.has_value():
      prod.set_value(m1.value * m2.value, self)
    elif prod.has_value() and m1.has_value():
      m2.set_value(prod.value / m1.value, self)
      pass
    elif prod.has_value() and m2.has_value():
      m1.set_value(prod.value / m2.value, self)

  def forget(self):
    self.prod.forget(self)
    self.m1.forget(self)
    self.m2.forget(self)
    self.process()

class squarer:
  def __init__(self, v1_, v2_, name_ = "unnamed squarer"):
    self.v1 = v1_
    self.v2 = v2_
    self.name = name_
    v1_.connect(self)
    v2_.connect(self)

  def process(self):
    v1,v2 = self.v1, self.v2
    if v1.value:
      v2.set_value(v1.value ** 2, self)
    elif v2.value:
      v1.set_value(math.sqrt(v2.value), self)

  def forget(self):
    self.v1.forget(self)
    self.v2.forget(self)
    self.process()


""" Test case"""
