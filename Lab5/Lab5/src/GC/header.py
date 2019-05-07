def header_get_garbage_flag(heap, pointer): 
    return ((heap[pointer+3] & 128) % 127) == 1

def header_set_garbage_flag(heap, pointer, value):
    pass

def header_get_used_flag(heap, pointer):
    return ((heap[pointer+3] & 64) % 63) == 1

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
