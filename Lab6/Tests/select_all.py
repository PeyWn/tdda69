#!/usr/bin/env python3

import SQpy
import unittest
import common

class SelectAll(unittest.TestCase):
  def test_select_all(self):
    db = common.fill_tables_1()
    
    # SELECT * FROM cities
    query1 = SQpy.ast.select(SQpy.ast.star(), from_table='cities')
    result1 = list(db.execute(query1))
    self.assertEqual(len(result1), 4)
    self.assertEqual(result1[0]._asdict(), {'name': 'Linkoping', 'population': 152966, 'longitude': 58.410833, 'latitude': 15.621389, 'country': 'Sweden', 'comment': 'My home town'})
    self.assertEqual(result1[1]._asdict(), {'name': 'Paris', 'population': 11836970, 'longitude': 48.85, 'latitude': 2.35, 'country': 'France', 'comment': None})
    self.assertEqual(result1[2]._asdict(), {'name': 'Strasbourg', 'population': 768868, 'longitude': 48.58, 'latitude': 7.75, 'country': 'France', 'comment': None})
    self.assertEqual(result1[3]._asdict(), {'name': 'London', 'population': 8538689, 'longitude': 51.507222, 'latitude': -0.1275, 'country': 'United Kingdom', 'comment': None})
    
    # SELECT name,population FROM cities
    query2 = SQpy.ast.select(['name', 'population'], from_table='cities')
    result2 = list(db.execute(query2))
    self.assertEqual(len(result2), 4)
    self.assertEqual(result2[0]._asdict(), {'name': 'Linkoping', 'population': 152966})
    self.assertEqual(result2[1]._asdict(), {'name': 'Paris', 'population': 11836970})
    self.assertEqual(result2[2]._asdict(), {'name': 'Strasbourg', 'population': 768868})
    self.assertEqual(result2[3]._asdict(), {'name': 'London', 'population': 8538689})



if __name__ == '__main__':
  unittest.main()

