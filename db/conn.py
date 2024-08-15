import psycopg2 
from utils.vars import DBNAME, USER, PASSWORD, HOST

PLAYERS_CONNECTION = psycopg2.connect(
  dbname='admin-players-dev',
  user=USER,
  password=PASSWORD,
  host=HOST,
)

ADMIN_CONNECTION = psycopg2.connect(
  dbname='admindb-dev',
  user=USER,
  password=PASSWORD,
  host=HOST,
)