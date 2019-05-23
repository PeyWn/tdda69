#!/usr/bin/env python3

import SQpy
import unittest
import common

class Insert(unittest.TestCase):
  def test_insert(self):
    db = common.create_tables()
    
    # INSERT INTO cities VALUES 'Linkoping', 152966, 58.410833, 15.621389, 'Sweden', 'My home town';
    query1 = SQpy.ast.insert_into('cities', values = ['Linkoping', 152966, 58.410833, 15.621389, 'Sweden', 'My home town'])
    db.execute(query1)
    
    self.assertEqual(len(db.dump_table('cities')), 1)
    self.assertEqual(len(db.dump_table('countries')), 0)
    self.assertEqual(db.dump_table('cities')[0]._asdict(), {'name': 'Linkoping', 'population': 152966, 'longitude': 58.410833, 'latitude': 15.621389, 'country': 'Sweden', 'comment': 'My home town'})
    
    # INSERT INTO cities (name, population, longitude, latitude, country) VALUES 'Paris', 11836970, 48.85, 2.35, 'France';
    query2 = SQpy.ast.insert_into('cities', columns = ['name', 'population', 'longitude', 'latitude', 'country'], values = ['Paris', 11836970, 48.85, 2.35, 'France'])
    db.execute(query2)

    self.assertEqual(len(db.dump_table('cities')), 2)
    self.assertEqual(len(db.dump_table('countries')), 0)
    self.assertEqual(db.dump_table('cities')[0]._asdict(), {'name': 'Linkoping', 'population': 152966, 'longitude': 58.410833, 'latitude': 15.621389, 'country': 'Sweden', 'comment': 'My home town'})
    self.assertEqual(db.dump_table('cities')[1]._asdict(), {'name': 'Paris', 'population': 11836970, 'longitude': 48.85, 'latitude': 2.35, 'country': 'France', 'comment': None})
    
    # INSERT INTO countries VALUES 'Sweden', 9858794;
    query3 = SQpy.ast.insert_into('countries', values = ['Sweden', 9858794])
    db.execute(query3)
    # INSERT INTO countries VALUES 'France', 64513000;
    query4 = SQpy.ast.insert_into('countries', values = ['France', 64513000])
    db.execute(query4)

    self.assertEqual(len(db.dump_table('cities')), 2)
    self.assertEqual(len(db.dump_table('countries')), 2)
    self.assertEqual(db.dump_table('cities')[0]._asdict(), {'name': 'Linkoping', 'population': 152966, 'longitude': 58.410833, 'latitude': 15.621389, 'country': 'Sweden', 'comment': 'My home town'})
    self.assertEqual(db.dump_table('cities')[1]._asdict(), {'name': 'Paris', 'population': 11836970, 'longitude': 48.85, 'latitude': 2.35, 'country': 'France', 'comment': None})
    self.assertEqual(db.dump_table('countries')[0]._asdict(), {'name': 'Sweden', 'population': 9858794 })
    self.assertEqual(db.dump_table('countries')[1]._asdict(), {'name': 'France', 'population': 64513000 })

if __name__ == '__main__':
  unittest.main()
 
