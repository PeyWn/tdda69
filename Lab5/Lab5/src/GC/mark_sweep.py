from .header import *
from .pointers_array import *

class mark_sweep(object):
  def __init__(self, heap):
    self.heap = heap
  # This function should collect the memory in the heap
  def collect(self):

    self.mark(0)

    header_ptr = 0
    while(header_ptr != -1):
      if not header_get_garbage_flag(self.heap.data, header_ptr):
        header_ptr = self.heap.disallocate(header_ptr)

      header_ptr = self.heap.get_next_header_pointer(header_ptr)

  def __rec_collect(self, pointer):
    pass

  def mark(self, root_ptr):
    if header_get_garbage_flag(self.heap.data, root_ptr):
        return

    self.heap.data = header_set_garbage_flag(self.heap.data, root_ptr, 1)

    if not header_is_pointers_array(self.heap.data, root_ptr):
        return

    root_ptr_count = pointer_array_count(self.heap.data, root_ptr)
    for i in range(root_ptr_count):
      root_obj = pointer_array_get(self.heap.data, root_ptr, i)
      print(root_obj)
      self.mark(root_obj)
