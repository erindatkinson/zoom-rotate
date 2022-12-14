from sqlite3 import Connection, connect
from os.path import join
from contextlib import closing
from os import listdir, remove
from os.path import splitext
from shutil import move

def db_conn(config:dict) -> Connection:
  """creates a connection object to the database"""
  return connect(config["db_location"])

def create(conn: Connection) -> None:
  """creates a table in the database if one doesn't already exist."""
  conn.cursor().execute("CREATE TABLE IF NOT EXISTS pictures (id int, approved bool, rejected bool)")
  conn.commit()

def find_picture(conn: Connection, img_id: int) -> tuple:
  """returns a record of the image requested, or None if no record exists"""
  cursor = conn.cursor()
  cursor.execute("SELECT * FROM pictures WHERE id=? LIMIT 1", (img_id,))
  return cursor.fetchone()

def add_picture(conn: Connection, img_id: int) -> None:
  """inserts an initial, unmarked record for the image into the database"""
  conn.cursor().execute("INSERT INTO pictures VALUES (?, ?, ?)", (img_id, False, False))
  conn.commit()

def approve_picture(conn: Connection, img_id: int) -> None:
  """updates the database entry for the image to be marked as approved"""
  conn.cursor().execute("UPDATE pictures set approved=? WHERE id=?", (True, img_id))
  conn.commit()

def reject_picture(conn: Connection, img_id: int) -> None:
  """updates the database entry for the image to be marked as rejected"""
  conn.cursor().execute("UPDATE pictures set rejected=? WHERE id=?", (True, img_id))
  conn.commit()

def mark_pictures(selection:tuple, action:str, config:dict) -> None:
  """Takes a tuple of int ids for image files, and an action (either 'approve' or 'reject') and for each image in the selection
  either moves the corresponding image to the approved directory, or deletes the image. It then updates the db record
  for the image id to match the action.
  """
  pending_dir = join(config["base_dir"], "images")
  approval_dir = join(config["base_dir"], "approved")
  pending = [i for i in listdir(pending_dir) if i !=".DS_Store"]

  with closing(db_conn(config)) as conn:
    for image in pending:
      id, ext = splitext(image)
      if int(id) in selection:
        if action == "reject":
          remove(join(pending_dir, image))
          reject_picture(conn, int(id))
        elif action == "accept":
          move(join(pending_dir, image), join(approval_dir))
          approve_picture(conn, int(id))
