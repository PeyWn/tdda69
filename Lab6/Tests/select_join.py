#!/usr/bin/env python3

import SQpy
import unittest
import common

class SelectJoin(unittest.TestCase):
  def test_select_inner_join(self):
    db = common.fill_tables_8()
    
    # SELECT cities.name AS name, cities.population / countries.population AS proportion FROM cities LEINNERFT JOIN countries ON cities.country = countries.name
    query1 = SQpy.ast.select(
                  [(SQpy.ast.identifier('cities', 'name'), 'name'), (SQpy.ast.op_divide( SQpy.ast.identifier('cities', 'population'), SQpy.ast.identifier('countries', 'population')), 'proportion')],
                  from_table = 'cities',
                  joins=[SQpy.ast.inner_join('countries',
                        on=SQpy.ast.op_equal(SQpy.ast.identifier('cities', 'country'), SQpy.ast.identifier('countries', 'name')))])


    result1 = list(db.execute(query1))
    self.assertEqual(len(result1), 3)
    self.assertEqual(result1[0]._asdict(), {'name': 'Linkoping', 'proportion': 0.015515690864420131})
    self.assertEqual(result1[1]._asdict(), {'name': 'Paris', 'proportion': 0.18348193387379289})
    self.assertEqual(result1[2]._asdict(), {'name': 'Strasbourg', 'proportion': 0.011918032024553191})
    
    # SELECT neighbourhoods.name AS name, neighbourhoods.population / countries.population AS proportion FROM cities INNER JOIN countries ON cities.country = countries.name INNER JOIN neighbourhoods ON neighbourhoods.city = cities.name
    query2 = SQpy.ast.select(
                  [(SQpy.ast.identifier('neighbourhoods', 'name'), 'name'), (SQpy.ast.op_divide( SQpy.ast.identifier('neighbourhoods', 'population'), SQpy.ast.identifier('countries', 'population')), 'proportion')],
                  from_table = 'cities',
                  joins=[SQpy.ast.inner_join('countries',
                        on=SQpy.ast.op_equal(SQpy.ast.identifier('cities', 'country'), SQpy.ast.identifier('countries', 'name'))),
                         SQpy.ast.inner_join('neighbourhoods',
                        on=SQpy.ast.op_equal(SQpy.ast.identifier('neighbourhoods', 'city'), SQpy.ast.identifier('cities', 'name'))) ])

    result2 = list(db.execute(query2))
    self.assertEqual(len(result2), 5)
    self.assertEqual(result2[0]._asdict(), {'name': 'Berga', 'proportion': 0.0006775676619270065})
    self.assertEqual(result2[1]._asdict(), {'name': 'Lambohov', 'proportion': 0.0008961542354977699})
    self.assertEqual(result2[2]._asdict(), {'name': '9th arrondissement', 'proportion': 0.0008655309782524453})
    self.assertEqual(result2[3]._asdict(), {'name': 'Cronenbourg', 'proportion': 0.0003330336521321284})
    self.assertEqual(result2[4]._asdict(), {'name': 'Neuhof', 'proportion': 0.0002587540495714042})


if __name__ == '__main__':
  unittest.main()

 
 
