

def unsigned_shift_right(v, s):
  if(v < 0):
    return (v & (2**32-1)) >> s
  return v >> s

