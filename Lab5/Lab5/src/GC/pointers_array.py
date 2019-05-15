from .header import *
import GC

def pointer_array_count(heap, pointer):
  return header_get_size(heap, pointer)/4

def pointer_array_get(heap, pointer, index):
  return int.from_bytes(heap[pointer+4+index*4:pointer+8+index*4], byteorder='little')

def pointer_array_set(heap, pointer, index, value):
  pos = pointer+4+index*4
  heap[pos] = value & 255
  heap[pos+1] = (value >> 8) & 255
  heap[pos+2] = (value >> 16) & 255
  heap[pos+3] = (value >> 24) & 255
  return heap
