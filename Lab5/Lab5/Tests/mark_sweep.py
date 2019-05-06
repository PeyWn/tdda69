#!/usr/bin/env python3

import GC
import unittest
 
class mark_sweep(unittest.TestCase):
  def test_it(self):
    heap = GC.heap(1000)
    
    root  = heap.allocate_array(6)
    obj1  = heap.allocate_bytes(23)
    obj2  = heap.allocate_array(3)
    obj3  = heap.allocate_bytes(141)
    obj4  = heap.allocate_array(6)
    obj5  = heap.allocate_array(12)
    obj6  = heap.allocate_array(4)
    obj7  = heap.allocate_array(2)
    obj8  = heap.allocate_array(22)
    obj9  = heap.allocate_array(9)
    obj10 = heap.allocate_bytes(2)
    obj11 = heap.allocate_bytes(5)
    obj12 = heap.allocate_bytes(9)
    obj13 = heap.allocate_bytes(4)
    obj14 = heap.allocate_bytes(7)
    obj15 = heap.allocate_bytes(11)
    
    GC.pointer_array_set(heap.data, root, 0, obj1)
    GC.pointer_array_set(heap.data, root, 1, obj2)
    GC.pointer_array_set(heap.data, root, 2, obj5)
    GC.pointer_array_set(heap.data, obj5, 5, obj6)
    GC.pointer_array_set(heap.data, root, 3, obj7)
    GC.pointer_array_set(heap.data, obj6, 2, obj7)
    GC.pointer_array_set(heap.data, obj6, 3, obj8)
    GC.pointer_array_set(heap.data, obj2, 0, obj10)
    GC.pointer_array_set(heap.data, obj8, 3, obj12)
    GC.pointer_array_set(heap.data, obj8, 7, obj14)
    # Disconnected and cyclic
    GC.pointer_array_set(heap.data, obj4, 0, obj9)
    GC.pointer_array_set(heap.data, obj9, 0, obj4)
    GC.pointer_array_set(heap.data, obj4, 1, obj15)
    GC.pointer_array_set(heap.data, obj9, 0, obj14)
    
    gc = GC.mark_sweep(heap)
    gc.collect()
    self.assertTrue(GC.header_get_used_flag(heap.data, root))
    self.assertTrue(GC.header_get_used_flag(heap.data, obj1))
    self.assertTrue(GC.header_get_used_flag(heap.data, obj2))
    self.assertFalse(GC.header_get_used_flag(heap.data, obj3))
    self.assertFalse(GC.header_get_used_flag(heap.data, obj4))
    self.assertTrue(GC.header_get_used_flag(heap.data, obj5))
    self.assertTrue(GC.header_get_used_flag(heap.data, obj6))
    self.assertTrue(GC.header_get_used_flag(heap.data, obj7))
    self.assertTrue(GC.header_get_used_flag(heap.data, obj8))
    self.assertFalse(GC.header_get_used_flag(heap.data, obj9))
    self.assertTrue(GC.header_get_used_flag(heap.data, obj10))
    self.assertFalse(GC.header_get_used_flag(heap.data, obj11))
    self.assertTrue(GC.header_get_used_flag(heap.data, obj12))
    self.assertFalse(GC.header_get_used_flag(heap.data, obj13))
    self.assertTrue(GC.header_get_used_flag(heap.data, obj14))
    self.assertFalse(GC.header_get_used_flag(heap.data, obj15))

if __name__ == '__main__':
  unittest.main()
