from .header import *
from .pointers_array import *

class heap(object):
  # size: the size (in bytes) of the heap
  def __init__(self, size):
    self.data             = bytearray(size)
    self.data             = header_set_size(self.data, 0, size-4)
    pass

  '''
  return the index to the begining of a block with size (in bytes)

  free_space: a list of tuples where index 0 is a pointer to a header
  and index 1 the headers size
  '''
  def allocate(self, size):
    free_space = self.free_space('Before alloc')
    success = False
    tail_header = max(free_space, key=lambda elem:elem[0])
    best_fit = max(free_space, key=lambda elem:elem[1])
    for space in free_space:
      if abs(space[1] - size) < best_fit[1]:
        best_fit = space
        success = True
    if success:
      new_tail_header = False
      if tail_header == best_fit[0]:
          new_tail_header = True

      if size < best_fit[1]:
        diff = best_fit[1] - size
        if diff >= 4:
          new_tail_header = True
        else:
          # if small diff allocate larger array
          size = size + diff

      self.set_used_and_size(best_fit[0], size, best_fit[1], new_tail_header)
      self.free_space('After alloc')
      print()
      return best_fit[0]
    return -1

  def set_used_and_size(self, pointer, allocated_size, total_size, new_tail_header = False):
      self.data = header_set_used_flag(self.data, pointer, 1)
      self.data = header_set_size(self.data, pointer, allocated_size)

      if new_tail_header:
        next_header = self.get_next_header_pointer(pointer)
        self.data = header_set_used_flag(self.data, next_header, 0)
        self.data = header_set_size(self.data, next_header, total_size-allocated_size-4)

  # unallocate the memory at the given index
  def disallocate(self, pointer):
    self.data = header_set_used_flag(self.data, pointer, 0)

    loop = True
    while(loop):
      loop = False
      free_space = self.free_space('Dealloc')
      for e in range(len(free_space)-1):
        if sum(free_space[e])+4 == free_space[e+1][0]:
          pointer = free_space[e][0]
          next_header = free_space[e+1][0]
          size = header_get_size(self.data, pointer)
          next_size = header_get_size(self.data, next_header)
          self.data = header_set_size(self.data, pointer, size+next_size+4)
          loop = True

    count = pointer_array_count(self.data, pointer)
    for i in range(count):
        self.data = pointer_array_set(self.data, pointer, i, 0)


  def free_space(self, msg = ''):
      header = 0
      free_space = []
      while(header != -1):
        header_size = header_get_size(self.data, header)
        if header_get_used_flag(self.data, header) == 0:
          free_space.append((header, header_size))
        header = self.get_next_header_pointer(header)
      print(msg, free_space)
      return free_space

  # Return the current total (allocatable) free space
  def total_free_space(self):
    return sum([e[1] for e in self.find_blocks(self.data, 0)])

  # Return the current total allocated memory
  def total_allocated_space(self):
    return sum([e[1] for e in self.find_blocks(self.data, 1)])

  def allocate_array(self, count):
    pointer = self.allocate(count * 4)
    header_mark_as_pointers_array(self.data, pointer)
    return pointer

  def allocate_bytes(self, count):
    pointer = self.allocate(count)
    header_mark_as_bytes_array(self.data, pointer)
    return pointer

  def get_next_header_pointer(self, pointer):
    #TODO size of block form header to index
    new_pointer = pointer + 4 + header_get_size(self.data, pointer)
    if new_pointer >= len(self.data):
      return -1
    return new_pointer

  '''
  Returns a list with header pointers and block size

  used or not; 0,1
  '''
  def find_blocks(self, data, used):
    pointer = 0
    blocks  = []
    while( pointer != -1 ):
      header_size = header_get_size(self.data, pointer)

      if header_get_used_flag(self.data, pointer) == used:
        blocks.append((pointer, header_size))

      pointer = self.get_next_header_pointer(pointer)

    return blocks
