import SQpy

def create_tables():
  db    = SQpy.database()
  # CREATE TABLE cities (name, population, longitude, latitude, country, comment)
  query = SQpy.ast.create_table('cities', ['name', 'population', 'longitude', 'latitude', 'country', 'comment'])
  db.execute(query)
  
  # CREATE TABLE countries (name, population)
  query = SQpy.ast.create_table('countries', ['name', 'population'])
  db.execute(query)

  return db

def fill_tables_1():
  db    = create_tables()
  
  # INSERT INTO cities VALUES 'Linkoping', 152966, 58.410833, 15.621389, 'Sweden', 'My home town';
  db.execute(SQpy.ast.insert_into('cities', values = ['Linkoping', 152966, 58.410833, 15.621389, 'Sweden', 'My home town']))
  # INSERT INTO cities (name, population, longitude, latitude, country) VALUES 'Paris', 11836970, 48.85, 2.35, 'France';
  db.execute(SQpy.ast.insert_into('cities', values = ['Paris', 11836970, 48.85, 2.35, 'France', None]))
  # INSERT INTO cities (name, population, longitude, latitude, country) VALUES 'Paris', 11836970, 48.85, 2.35, 'France';
  db.execute(SQpy.ast.insert_into('cities', values = ['Strasbourg', 768868, 48.58, 7.75, 'France', None]))
  # INSERT INTO cities (name, population, longitude, latitude, country) VALUES 'Paris', 11836970, 48.85, 2.35, 'France';
  db.execute(SQpy.ast.insert_into('cities', values = ['London', 8538689, 51.507222, -0.1275, 'United Kingdom', None]))
  
  # INSERT INTO countries VALUES 'Sweden', 9858794;
  db.execute(SQpy.ast.insert_into('countries', values = ['Sweden', 9858794]))
  # INSERT INTO countries VALUES 'France', 64513000;
  db.execute(SQpy.ast.insert_into('countries', values = ['France', 64513000]))
  
  return db

def fill_tables_8():
  db = fill_tables_1()

  # CREATE TABLE neighbourhoods (name, population)
  query = SQpy.ast.create_table('neighbourhoods', ['name', 'population', 'city'])
  db.execute(query)

  # INSERT INTO neighbourhoods VALUES 'Berga', 6680, 'Linkoping';
  db.execute(SQpy.ast.insert_into('neighbourhoods', values = ['Berga', 6680, 'Linkoping']))

  # INSERT INTO neighbourhoods VALUES 'Lambohov', 8835, 'Linkoping';
  db.execute(SQpy.ast.insert_into('neighbourhoods', values = ['Lambohov', 8835, 'Linkoping']))

  # INSERT INTO neighbourhoods VALUES '9th arrondissement', 55838, 'Paris';
  db.execute(SQpy.ast.insert_into('neighbourhoods', values = ['9th arrondissement', 55838, 'Paris']))

  # INSERT INTO neighbourhoods VALUES 'Cronenbourg', 21485, 'Strasbourg';
  db.execute(SQpy.ast.insert_into('neighbourhoods', values = ['Cronenbourg', 21485, 'Strasbourg']))

  # INSERT INTO neighbourhoods VALUES 'Neuhof', 16693, 'Strasbourg';
  db.execute(SQpy.ast.insert_into('neighbourhoods', values = ['Neuhof', 16693, 'Strasbourg']))

  # INSERT INTO neighbourhoods VALUES 'Greenwich', 268678, 'London';
  db.execute(SQpy.ast.insert_into('neighbourhoods', values = ['Greenwich', 268678, 'London']))

  return db
