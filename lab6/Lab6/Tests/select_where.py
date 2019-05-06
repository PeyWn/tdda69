#!/usr/bin/env python3

import SQpy
import unittest
import common

class SelectWhere(unittest.TestCase):
  def test_select_where(self):
    db = common.fill_tables_1()
    
    # SELECT name,population FROM cities WHERE population > 1000000
    query1 = SQpy.ast.select(['name', 'population'], from_table='cities',
          where=SQpy.ast.op_superior(
                        SQpy.ast.identifier('population'), 1000000))

    result1 = list(db.execute(query1))
    self.assertEqual(len(result1), 2)
    self.assertEqual(result1[0]._asdict(), {'name': 'Paris', 'population': 11836970})
    self.assertEqual(result1[1]._asdict(), {'name': 'London', 'population': 8538689})

if __name__ == '__main__':
  unittest.main()

 
