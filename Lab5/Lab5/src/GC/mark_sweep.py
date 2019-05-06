from .header import * 
from .pointers_array import *

class mark_sweep(object):
  def __init__(self, heap):
    self.heap = heap
  # This function should collect the memory in the heap
  def collect(self):
    pass

  def __rec_collect(self, pointer):
    pass
