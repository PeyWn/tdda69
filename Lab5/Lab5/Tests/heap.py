#!/usr/bin/env python3

import GC
import unittest

class Heap(unittest.TestCase):
  def test_allocation(self):
    heap = GC.heap(1000)
    self.assertEqual(heap.total_free_space(), 996)
    self.assertEqual(heap.total_allocated_space(), 0)
    
    self.assertFalse(GC.header_get_used_flag(heap.data, 0))
    self.assertEqual(GC.header_get_size(heap.data, 0), 996)
    
    # Allocate a chunk of memory
    pointer = heap.allocate(10)
    self.assertEqual(heap.total_free_space(), 982)
    self.assertEqual(heap.total_allocated_space(), 10)
    
    self.assertEqual(pointer, 0)
    self.assertTrue(GC.header_get_used_flag(heap.data, pointer))
    self.assertEqual(GC.header_get_size(heap.data, pointer), 10)
    next_free_pointer = pointer + 14
    self.assertFalse(GC.header_get_used_flag(heap.data, next_free_pointer))
    self.assertEqual(GC.header_get_size(heap.data, next_free_pointer), 982)
    
    # Allocate more memory
    pointer = heap.allocate(12)
    self.assertEqual(heap.total_free_space(), 966)
    self.assertEqual(heap.total_allocated_space(), 22)
    
    self.assertEqual(pointer, 14)
    self.assertTrue(GC.header_get_used_flag(heap.data, pointer))
    self.assertEqual(GC.header_get_size(heap.data, pointer), 12)
    next_free_pointer = pointer + 16
    self.assertFalse(GC.header_get_used_flag(heap.data, next_free_pointer))
    self.assertEqual(GC.header_get_size(heap.data, next_free_pointer), 966)

  def test_desallocation_simple(self):
    heap = GC.heap(1000)
    
    pointer1 = heap.allocate(10)
    pointer2 = heap.allocate(12)
    pointer3 = heap.allocate(30)
    
    self.assertEqual(pointer1, 0)
    self.assertEqual(pointer2, 14)
    self.assertEqual(pointer3, 30)

    self.assertEqual(heap.total_free_space(), 932)
    self.assertEqual(heap.total_allocated_space(), 52)
    
    heap.disallocate(pointer3)
    
    self.assertEqual(heap.total_free_space(), 966)
    self.assertEqual(heap.total_allocated_space(), 22)
    self.assertEqual(GC.header_get_size(heap.data, pointer3), 966)
    self.assertFalse(GC.header_get_used_flag(heap.data, pointer3))

    heap.disallocate(pointer2)
    
    self.assertEqual(heap.total_free_space(), 982)
    self.assertEqual(heap.total_allocated_space(), 10)
    self.assertEqual(GC.header_get_size(heap.data, pointer2), 982)
    self.assertFalse(GC.header_get_used_flag(heap.data, pointer2))
    for i in range(0, 8):
      self.assertEqual(heap.data[pointer3 + i], 0)

    heap.disallocate(pointer1)
    
    self.assertEqual(heap.total_free_space(), 996)
    self.assertEqual(heap.total_allocated_space(), 0)
    self.assertEqual(GC.header_get_size(heap.data, pointer1), 996)
    self.assertFalse(GC.header_get_used_flag(heap.data, pointer1))
    for i in range(0, 8):
      self.assertEqual(heap.data[pointer2 + i], 0)

  def test_desallocation_complex_1(self):

    heap = GC.heap(1000)
    
    pointer1 = heap.allocate(10)
    pointer2 = heap.allocate(12)
    pointer3 = heap.allocate(30)
    
    self.assertEqual(pointer1, 0)
    self.assertEqual(pointer2, 14)
    self.assertEqual(pointer3, 30)

    self.assertEqual(heap.total_free_space(), 932)
    self.assertEqual(heap.total_allocated_space(), 52)

    heap.disallocate(pointer2)
    
    self.assertEqual(heap.total_free_space(), 944)
    self.assertEqual(heap.total_allocated_space(), 40)
    self.assertEqual(GC.header_get_size(heap.data, pointer2), 12)
    self.assertFalse(GC.header_get_used_flag(heap.data, pointer2))
    
    heap.disallocate(pointer3)
    
    self.assertEqual(heap.total_free_space(), 982)
    self.assertEqual(heap.total_allocated_space(), 10)
    self.assertEqual(GC.header_get_size(heap.data, pointer2), 982)
    self.assertFalse(GC.header_get_used_flag(heap.data, pointer2))
    for i in range(0, 8):
      self.assertEqual(heap.data[pointer3 + i], 0)

    pointer2 = heap.allocate(12)
    pointer3 = heap.allocate(30)
    self.assertEqual(pointer2, 14)
    self.assertEqual(pointer3, 30)

    self.assertEqual(heap.total_free_space(), 932)
    self.assertEqual(heap.total_allocated_space(), 52)

    heap.disallocate(pointer2)
    
    self.assertEqual(heap.total_free_space(), 944)
    self.assertEqual(heap.total_allocated_space(), 40)
    self.assertEqual(GC.header_get_size(heap.data, pointer2), 12)
    self.assertFalse(GC.header_get_used_flag(heap.data, pointer2))

    heap.disallocate(pointer1)
    
    self.assertEqual(heap.total_free_space(), 958)
    self.assertEqual(heap.total_allocated_space(), 30)
    self.assertEqual(GC.header_get_size(heap.data, pointer1), 26)
    self.assertFalse(GC.header_get_used_flag(heap.data, pointer1))
    for i in range(0, 8):
      self.assertEqual(heap.data[pointer2 + i], 0)
    
  def test_desallocation_complex_2(self):
    heap = GC.heap(1000)

    pointer1 = heap.allocate(10)
    pointer2 = heap.allocate(12)
    pointer3 = heap.allocate(30)
    pointer4 = heap.allocate(18)
    pointer5 = heap.allocate(12)
    
    self.assertEqual(pointer1, 0)
    self.assertEqual(pointer2, 14)
    self.assertEqual(pointer3, 30)
    self.assertEqual(pointer4, 64)
    self.assertEqual(pointer5, 86)
    
    self.assertEqual(heap.total_free_space(), 894)
    self.assertEqual(heap.total_allocated_space(), 82)
    
    heap.disallocate(pointer1)
    heap.disallocate(pointer3)
    self.assertEqual(GC.header_get_size(heap.data, pointer1), 10)
    self.assertFalse(GC.header_get_used_flag(heap.data, pointer1))
    self.assertEqual(GC.pointer_array_get(heap.data, pointer1, 0), pointer3)
    self.assertEqual(GC.header_get_size(heap.data, pointer3), 30)
    self.assertFalse(GC.header_get_used_flag(heap.data, pointer3))
    self.assertEqual(GC.pointer_array_get(heap.data, pointer3, 0), pointer5 + 16)
    
    heap.disallocate(pointer4)
    self.assertEqual(GC.header_get_size(heap.data, pointer1), 10)
    self.assertFalse(GC.header_get_used_flag(heap.data, pointer1))
    self.assertEqual(GC.header_get_size(heap.data, pointer3), 52)
    self.assertFalse(GC.header_get_used_flag(heap.data, pointer3))
    self.assertEqual(GC.pointer_array_get(heap.data, pointer3, 0), pointer5 + 16)
    
    pointer1 = heap.allocate(10)
    self.assertEqual(pointer1, 0)
    heap.disallocate(pointer1)
    
    pointer3 = heap.allocate(30)
    self.assertTrue(GC.header_get_used_flag(heap.data, pointer3))
    self.assertEqual(GC.header_get_size(heap.data, pointer3), 30)
    self.assertEqual(GC.pointer_array_get(heap.data, pointer1, 0), pointer4)
    
    pointer4 = heap.allocate(18)
    
    self.assertEqual(pointer1, 0)
    self.assertEqual(pointer2, 14)
    self.assertEqual(pointer3, 30)
    self.assertEqual(pointer4, 64)
    self.assertEqual(pointer5, 86)

    heap.disallocate(pointer3)
    heap.disallocate(pointer5)
    self.assertEqual(GC.header_get_size(heap.data, pointer1), 10)
    self.assertFalse(GC.header_get_used_flag(heap.data, pointer1))
    self.assertEqual(GC.header_get_size(heap.data, pointer3), 30)
    self.assertFalse(GC.header_get_used_flag(heap.data, pointer3))
    self.assertEqual(GC.pointer_array_get(heap.data, pointer3, 0), pointer5)
  
  def test_best_fit(self):
    heap = GC.heap(1000)

    pointer1 = heap.allocate(10)
    pointer2 = heap.allocate(18)
    pointer3 = heap.allocate(30)
    pointer4 = heap.allocate(12)
    pointer5 = heap.allocate(12)
    
    self.assertEqual(pointer1, 0)
    self.assertEqual(pointer2, 14)
    self.assertEqual(pointer3, 36)
    self.assertEqual(pointer4, 70)
    self.assertEqual(pointer5, 86)
    
    heap.disallocate(pointer2)
    heap.disallocate(pointer4)
    
    pointer6 = heap.allocate(12)
    self.assertEqual(pointer6, 70)
    pointer7 = heap.allocate(16)
    self.assertEqual(pointer7, 102)

if __name__ == '__main__':
  unittest.main()
