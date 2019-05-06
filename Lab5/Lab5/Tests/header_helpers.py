#!/usr/bin/env python3

import GC
import unittest

class HeadersHelpers(unittest.TestCase):
  def test_header_get_garbage_flag(self):
    b = bytearray(b'\x10\x15\x12\x81\x51\x15\x12\x12\x45\x12\x52\x23\x23\x00\xd0\xff')

    self.assertTrue(GC.header_get_garbage_flag(b, 0))
    self.assertFalse(GC.header_get_garbage_flag(b, 4))
    self.assertFalse(GC.header_get_garbage_flag(b, 8))
    self.assertTrue(GC.header_get_garbage_flag(b, 12))
  def test_header_set_garbage_flag(self):
    b = bytearray(b'\x10\x15\x12\x81\x51\x15\x12\x12\x45\x12\x52\x23\x23\x00\xd0\xff')

    GC.header_set_garbage_flag(b, 0, False)
    GC.header_set_garbage_flag(b, 4, True)
    GC.header_set_garbage_flag(b, 8, True)
    GC.header_set_garbage_flag(b,12, False)

    self.assertFalse(GC.header_get_garbage_flag(b, 0))
    self.assertTrue(GC.header_get_garbage_flag(b, 4))
    self.assertTrue(GC.header_get_garbage_flag(b, 8))
    self.assertFalse(GC.header_get_garbage_flag(b, 12))
    self.assertEqual(b, bytearray(b'\x10\x15\x12\x01Q\x15\x12\x92E\x12R\xa3#\x00\xd0\x7f'))

  def test_header_get_used_flag(self):
    b = b'\x10\x15\x12\x81\x51\x15\x12\x12\x45\x12\x52\x23\x23\x00\xd0\xff'

    self.assertFalse(GC.header_get_used_flag(b, 0))
    self.assertFalse(GC.header_get_used_flag(b, 4))
    self.assertFalse(GC.header_get_used_flag(b, 8))
    self.assertTrue(GC.header_get_used_flag(b, 12))

  def test_header_set_used_flag(self):
    b = bytearray(b'\x10\x15\x12\x81\x51\x15\x12\x12\x45\x12\x52\x23\x23\x00\xd0\xff')

    GC.header_set_used_flag(b, 0, False)
    GC.header_set_used_flag(b, 4, True)
    GC.header_set_used_flag(b, 8, True)
    GC.header_set_used_flag(b,12, False)

    self.assertFalse(GC.header_get_used_flag(b, 0))
    self.assertTrue(GC.header_get_used_flag(b, 4))
    self.assertTrue(GC.header_get_used_flag(b, 8))
    self.assertFalse(GC.header_get_used_flag(b, 12))
    self.assertEqual(b, bytearray(b'\x10\x15\x12\x81Q\x15\x12RE\x12Rc#\x00\xd0\xbf'))

  def test_header_is_pointers_array(self):
    b = b'\x10\x15\x12\x81\x51\x15\x12\x12\x45\x12\x52\x23\x23\x00\xd0\xff'

    self.assertFalse(GC.header_is_pointers_array(b, 0))
    self.assertFalse(GC.header_is_pointers_array(b, 4))
    self.assertTrue(GC.header_is_pointers_array(b, 8))
    self.assertTrue(GC.header_is_pointers_array(b, 12))

  def test_header_mark(self):
    b = bytearray(b'\x10\x15\x12\x81\x51\x15\x12\x12\x45\x12\x52\x23\x23\x00\xd0\xff')

    GC.header_mark_as_pointers_array(b, 0)
    GC.header_mark_as_bytes_array(b, 4)
    GC.header_mark_as_pointers_array(b, 8)
    GC.header_mark_as_bytes_array(b,12)

    self.assertTrue(GC.header_is_pointers_array(b, 0))
    self.assertFalse(GC.header_is_pointers_array(b, 4))
    self.assertTrue(GC.header_is_pointers_array(b, 8))
    self.assertFalse(GC.header_is_pointers_array(b, 12))
    self.assertEqual(b, bytearray(b'\x10\x15\x12\xa1Q\x15\x12\x12E\x12R##\x00\xd0\xdf'))

  def test_header_get_size(self):
    b = bytearray(b'\x10\x15\x12\x81\x51\x15\x12\x12\x45\x12\x52\x23\x23\x00\xd0\xff')
    self.assertEqual(GC.header_get_size(b,0), 17962256 )
    self.assertEqual(GC.header_get_size(b,4), 303174993 )
    self.assertEqual(GC.header_get_size(b,8), 55710277)
    self.assertEqual(GC.header_get_size(b,12),533725219 )

  def test_header_set_size(self):
    b = bytearray(b'\x10\x15\x12\x81\x51\x15\x12\x12\x45\x12\x52\x23\x23\x00\xd0\xff')
    GC.header_set_size(b, 0, 12535)
    #GC.header_set_size(b, 4, 241)
    #GC.header_set_size(b, 8, 5334)
    #GC.header_set_size(b,12, 1242412)
    self.assertEqual(GC.header_get_size(b,0), 12535)
    #self.assertEqual(GC.header_get_size(b,4), 241)
    #self.assertEqual(GC.header_get_size(b,8), 5334)
    #self.assertEqual(GC.header_get_size(b,12), 1242412)

if __name__ == '__main__':
  unittest.main()
