import psycopg2 
from utils.vars import DBNAME, USER, PASSWORD, HOST

CONNECTION = psycopg2.connect(
  dbname=DBNAME,
  user=USER,
  password=PASSWORD,
  host=HOST,
)