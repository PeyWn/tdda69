#!/usr/bin/env python3

import SQpy
import unittest
import common
#from .common import create_tables
 
class Update(unittest.TestCase):
  def test_insert(self):
    db = common.create_tables()
    
    # INSERT INTO cities VALUES 'Linkoping', 152966, 58.410833, 15.621389, 'Sweden', 'My home town';
    query1 = SQpy.ast.insert_into('cities', values = ['Linkoping', 152966, 58.410833, 15.621389, 'Sweden', 'My home town'])
    db.execute(query1)
    # INSERT INTO cities (name, population, longitude, latitude, country) VALUES 'Paris', 11836970, 48.85, 2.35, 'France';
    query2 = SQpy.ast.insert_into('cities', columns = ['name', 'population', 'longitude', 'latitude', 'country'], values = ['Paris', 11836970, 48.85, 2.35, 'France'])
    db.execute(query2)
    # INSERT INTO cities (name, population, longitude, latitude, country) VALUES 'Paris', 11836970, 48.85, 2.35, 'France';
    query3 = SQpy.ast.insert_into('cities', columns = ['name', 'population', 'longitude', 'latitude', 'country'], values = ['Strasbourg', 768868, 48.58, 7.75, 'France'])
    db.execute(query3)
    # INSERT INTO cities (name, population, longitude, latitude, country) VALUES 'Paris', 11836970, 48.85, 2.35, 'France';
    query4 = SQpy.ast.insert_into('cities', columns = ['name', 'population', 'longitude', 'latitude', 'country'], values = ['London', 8538689, 51.507222,  -0.1275, 'United Kingdom'])
    db.execute(query4)

    self.assertEqual(len(db.dump_table('cities')), 4)
    self.assertEqual(db.dump_table('cities')[0]._asdict(), {'name': 'Linkoping', 'population': 152966, 'longitude': 58.410833, 'latitude': 15.621389, 'country': 'Sweden', 'comment': 'My home town'})
    self.assertEqual(db.dump_table('cities')[1]._asdict(), {'name': 'Paris', 'population': 11836970, 'longitude': 48.85, 'latitude': 2.35, 'country': 'France', 'comment': None})
    self.assertEqual(db.dump_table('cities')[2]._asdict(), {'name': 'Strasbourg', 'population': 768868, 'longitude': 48.58, 'latitude': 7.75, 'country': 'France', 'comment': None})
    self.assertEqual(db.dump_table('cities')[3]._asdict(), {'name': 'London', 'population': 8538689, 'longitude': 51.507222, 'latitude': -0.1275, 'country': 'United Kingdom', 'comment': None})
    
    # UPDATE cities SET comment = 'My birth town' WHERE name = 'Paris'
    query = SQpy.ast.update('cities', set=[('comment', 'My birth town')], where=SQpy.ast.op_equal(SQpy.ast.identifier('name'), 'Paris'))
    db.execute(query)
    
    self.assertEqual(len(db.dump_table('cities')), 4)
    self.assertEqual(db.dump_table('cities')[0]._asdict(), {'name': 'Linkoping', 'population': 152966, 'longitude': 58.410833, 'latitude': 15.621389, 'country': 'Sweden', 'comment': 'My home town'})
    self.assertEqual(db.dump_table('cities')[1]._asdict(), {'name': 'Paris', 'population': 11836970, 'longitude': 48.85, 'latitude': 2.35, 'country': 'France', 'comment': 'My birth town'})
    self.assertEqual(db.dump_table('cities')[2]._asdict(), {'name': 'Strasbourg', 'population': 768868, 'longitude': 48.58, 'latitude': 7.75, 'country': 'France', 'comment': None})
    self.assertEqual(db.dump_table('cities')[3]._asdict(), {'name': 'London', 'population': 8538689, 'longitude': 51.507222, 'latitude': -0.1275, 'country': 'United Kingdom', 'comment': None})

    query = SQpy.ast.update('cities', set=[('comment', 'My birth country'), ('country', 'Frankrike')], where=SQpy.ast.op_equal(SQpy.ast.identifier('country'), 'France'))
    db.execute(query)

    self.assertEqual(len(db.dump_table('cities')), 4)
    self.assertEqual(db.dump_table('cities')[0]._asdict(), {'name': 'Linkoping', 'population': 152966, 'longitude': 58.410833, 'latitude': 15.621389, 'country': 'Sweden', 'comment': 'My home town'})
    self.assertEqual(db.dump_table('cities')[1]._asdict(), {'name': 'Paris', 'population': 11836970, 'longitude': 48.85, 'latitude': 2.35, 'country': 'Frankrike', 'comment': 'My birth country'})
    self.assertEqual(db.dump_table('cities')[2]._asdict(), {'name': 'Strasbourg', 'population': 768868, 'longitude': 48.58, 'latitude': 7.75, 'country': 'Frankrike', 'comment': 'My birth country'})
    self.assertEqual(db.dump_table('cities')[3]._asdict(), {'name': 'London', 'population': 8538689, 'longitude': 51.507222, 'latitude': -0.1275, 'country': 'United Kingdom', 'comment': None})

if __name__ == '__main__':
  unittest.main()
 
 
 
