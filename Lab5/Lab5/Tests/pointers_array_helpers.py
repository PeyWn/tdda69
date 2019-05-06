#!/usr/bin/env python3

import GC
import unittest

class PointersArray(unittest.TestCase):
  def test_pointer_array_count(self):
    b = bytearray(b'\xf0\xff\xff\x0f\x80:"$DD3\xf2')
    self.assertEqual(GC.pointer_array_count(b, 0), 67108860)
    self.assertEqual(GC.pointer_array_count(b, 4), 17338016)
    self.assertEqual(GC.pointer_array_count(b, 8), 76337425)

  def test_pointer_array_get(self):
    b = bytearray(b'\xf0\xff\xff\x0f\x80:"$DD3\xf2')
    self.assertEqual(GC.pointer_array_get(b, 0, 0), 0x24223a80)
    self.assertEqual(GC.pointer_array_get(b, 0, 1), 0xf2334444)
    self.assertEqual(GC.pointer_array_get(b, 4, 0), 0xf2334444)
  
  def test_pointer_array_set(self):
    b = bytearray(12)
    GC.header_set_used_flag(b,0,True)
    GC.header_mark_as_pointers_array(b,0)
    GC.header_set_size(b, 0, 8)
    GC.pointer_array_set(b, 0, 0, 0x12345678)
    GC.pointer_array_set(b, 0, 1, 0xfedcba90)
    self.assertEqual(GC.pointer_array_count(b, 0), 2)
    self.assertEqual(GC.header_get_size(b, 0), 8)
    self.assertTrue(GC.header_is_pointers_array(b, 0))
    self.assertTrue(GC.header_get_used_flag(b, 0))
    self.assertEqual(GC.pointer_array_get(b, 0, 0), 0x12345678)
    self.assertEqual(GC.pointer_array_get(b, 0, 1), 0xfedcba90)
    self.assertEqual(b, bytearray(b'\x08\x00\x00`xV4\x12\x90\xba\xdc\xfe'))

if __name__ == '__main__':
  unittest.main()
