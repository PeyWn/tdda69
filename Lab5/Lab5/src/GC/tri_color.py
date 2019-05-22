from .header import *
from .pointers_array import *

class tri_color(object):
  def __init__(self, heap):
    self.heap = heap
    self.white = []
    self.gray = []
    self.black = []
  # This function should collect the memory in the heap
  def collect(self):

    # Collor all obj self.white
    pointer = 0
    while pointer != -1:
      self.white.append(pointer)
      pointer = self.heap.get_next_header_pointer(pointer)

    # Color all root set objs self.gray
    root_ptr = 0
    root_ptr_count = pointer_array_count(self.heap.data, root_ptr)
    for i in range(root_ptr_count-1):
      root_obj = pointer_array_get(self.heap.data, root_ptr, i)
      self.white.remove(root_obj)
      self.gray.append(root_obj)

    # Repeat mark self.black
    self.mark_black(root_ptr)

    # Free self.white
    for e in self.white:
      self.heap.disallocate(e)

    print(self.gray)


  def mark_black(self, root_ptr):
    if (not self.gray) or root_ptr in self.black:
      return

    self.gray.remove(root_ptr)
    self.black.append(root_ptr)
    if not header_is_pointers_array(self.heap.data, root_ptr):
      return

    root_ptr_count = pointer_array_count(self.heap.data, root_ptr)
    for i in range(root_ptr_count):
      root_obj = pointer_array_get(self.heap.data, root_ptr, i)
      if not root_obj in self.black:
        if root_obj in self.white:
          self.white.remove(root_obj)
          self.gray.append(root_obj)
        self.mark_black(root_obj)
