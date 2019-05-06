def header_get_garbage_flag(heap, pointer):
    print('1', heap)
    print('2', heap[-1-pointer])
    print('3', heap[-1-pointer] & 1)
    print('4', heap[-1-pointer] & 1 == 1)
    return heap[-1-pointer] & 1 == True


def header_set_garbage_flag(heap, pointer, value):
  pass

def header_get_used_flag(heap, pointer):
  pass

def header_set_used_flag(heap, pointer, value):
  pass

def header_is_pointers_array(heap, pointer):
  pass

def header_mark_as_pointers_array(heap, pointer):
  pass

def header_mark_as_bytes_array(heap, pointer):
  pass

def header_get_size(heap, pointer):
  pass

def header_set_size(heap, pointer, size):
  pass
