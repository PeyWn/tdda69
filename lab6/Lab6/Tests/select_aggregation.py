#!/usr/bin/env python3

import SQpy
import unittest
import common

class SelectAggregation(unittest.TestCase):
  def test_select_aggregation(self):
    db = common.fill_tables_1()
    
    # SELECT count(name) AS city_count, avg(population) AS avg_population FROM cities WHERE population > 1000000
    query = SQpy.ast.select([(SQpy.ast.count('name') , 'city_count'), (SQpy.ast.avg('population') , 'avg_population')],
                        from_table = 'cities', where=SQpy.ast.op_superior(
                            SQpy.ast.identifier('population'), 1000000))
    result = list(db.execute(query))
    self.assertEqual(len(result), 1)
    self.assertEqual(result[0]._asdict(), {'city_count': 2, 'avg_population': 10187829.5})



if __name__ == '__main__':
  unittest.main()

