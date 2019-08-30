import sqlite3
import os
from pathlib import Path

os.chdir(Path(__file__).parent)
path = os.path.join(os.getcwd(), 'db/default.db')
con = sqlite3.Connection(path)
table_name = "years"
con.row_factory = sqlite3.Row


cur = con.cursor()
cur.execute('SELECT * FROM '+ table_name)
print("TABLE: " + table_name)
for row in cur.fetchall():
    # can convert to dict if you want:
    print(dict(row))