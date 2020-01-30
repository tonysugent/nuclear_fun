import psycopg2

params = {
  'dbname': 'nuke',
  'user': 'tony',
  'password': 'rOflstomp11!',
  'host': '18.219.19.27',
  'port': 5432
}

conn = psycopg2.connect(**params)
cur = conn.cursor()
cur.execute('select * from countries')
print(cur.fetchone())