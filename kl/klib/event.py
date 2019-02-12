
class event:
  def __init__(self):
    self.listeners = []
  def trigger(self, **kargs):
    for l in self.listeners:
      l(**kargs)
  def listen(self, l):
    self.listeners.append(l)
  def unlisten(self, l):
    self.listeners.remove(l)