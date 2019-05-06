#!/usr/bin/env python3

import SQpy
import unittest
import common

class SelectAll(unittest.TestCase):
  def test_select_all(self):
    db = common.fill_tables_1()
    
    # SELECT name, population / 1000000 AS population_proportion FROM cities
    query = SQpy.ast.select(['name', (SQpy.ast.op_divide(SQpy.ast.identifier('population'), 1000000), 'population_proportion')], from_table = 'cities')
    result = list(db.execute(query))
    self.assertEqual(len(result), 4)
    self.assertEqual(result[0]._asdict(), {'name': 'Linkoping', 'population_proportion': 0.152966})
    self.assertEqual(result[1]._asdict(), {'name': 'Paris', 'population_proportion': 11.836970})
    self.assertEqual(result[2]._asdict(), {'name': 'Strasbourg', 'population_proportion': 0.768868})
    self.assertEqual(result[3]._asdict(), {'name': 'London', 'population_proportion': 8.538689})



if __name__ == '__main__':
  unittest.main()

 
