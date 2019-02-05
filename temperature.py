from constraints import Connector, Adder, Multiplier, Constant

# Defines a conversion network.
def temperature_converter(c,f):
  """Constrains C and F so that C.value is the same degrees Celsius as F.value is Farenheit"""
  u = Connector()
  v = Connector()
  w = Connector()
  x = Connector()
  y = Connector()
  Multiplier(c,w,u)
  Multiplier(v,x,u)
  Adder(v, y, f)
  Constant(9, w)
  Constant(5, x)
  Constant(32, y)
  print("Connected ", c.name, " with ",  f.name)

c = Connector("Celsius")
f = Connector("Farenheit")
temperature_converter(c,f)
c.show_updates = True
f.show_updates = True
c.set_value(100, "user")
c.forget("user")
f.set_value(123, "user")
f.forget("user")
