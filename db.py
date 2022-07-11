from sqlite3 import Connection, connect
from os.path import join

def db_conn(config:dict) -> Connection:
  return connect(config["db_location"])

def create(conn: Connection):
    conn.cursor().execute("CREATE TABLE IF NOT EXISTS pictures (id int, approved bool, rejected bool)")
    conn.commit()

def find_picture(conn: Connection, img_id: int) -> tuple: 
  cursor = conn.cursor()
  cursor.execute("SELECT * FROM pictures WHERE id=? LIMIT 1", (img_id,))
  return cursor.fetchone()

def add_picture(conn: Connection, img_id: int):
  conn.cursor().execute("INSERT INTO pictures VALUES (?, ?, ?)", (img_id, False, False))
  conn.commit()
