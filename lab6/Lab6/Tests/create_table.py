#!/usr/bin/env python3

import SQpy
import unittest
 
class CreateTable(unittest.TestCase):
  def test_create_table(self):
    # CREATE TABLE cities (name, population, longitude, latitude, country, comment)
    query = SQpy.ast.create_table('cities', ['name', 'population', 'longitude', 'latitude', 'country', 'comment'])
    db    = SQpy.database()
    db.execute(query)
    self.assertEqual(db.tables(), ['cities'])
    self.assertEqual(db.fields('cities'), ['name', 'population', 'longitude', 'latitude', 'country', 'comment'])
    
    # CREATE TABLE countries (name, population)
    query = SQpy.ast.create_table('countries', ['name', 'population'])
    
    db.execute(query)
    self.assertTrue('cities' in db.tables())
    self.assertTrue('countries' in db.tables())
    self.assertEqual(len(db.tables()), 2)
    self.assertEqual(db.fields('cities'), ['name', 'population', 'longitude', 'latitude', 'country', 'comment'])
    self.assertEqual(db.fields('countries'), ['name', 'population'])

if __name__ == '__main__':
  unittest.main()
