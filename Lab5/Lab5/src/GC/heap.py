from .header import * 
from .pointers_array import *

class heap(object):
  # size: the size (in bytes) of the heap
  def __init__(self, size):
    self.data             = bytearray(size)
    pass
  
  # return the index to the begining of a block with size (in bytes)
  def allocate(self, size):
    pass
  
  # unallocate the memory at the given index
  def disallocate(self, pointer):
    pass
  
  # Return the current total (allocatable) free space
  def total_free_space(self):
    pass
  
  # Return the current total allocated memory
  def total_allocated_space(self):
    pass

  def allocate_array(self, count):
    pointer = self.allocate(count * 4)
    header_mark_as_pointers_array(self.data, pointer)
    return pointer

  def allocate_bytes(self, count):
    pointer = self.allocate(count)
    header_mark_as_bytes_array(self.data, pointer)
    return pointer
