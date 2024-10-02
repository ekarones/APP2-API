import sqlite3
import os

if not os.path.exists("database/images"):
    os.makedirs("database/images")

conn = sqlite3.connect("database/app-db.sqlite")

cursor = conn.cursor()

with open("schema.sql", "r") as file:
    schema = file.read()

cursor.executescript(schema)

conn.commit()

conn.close()
