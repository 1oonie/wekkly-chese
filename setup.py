import sqlite3

with open("schema.sql") as fp:
    schema = fp.read()

connection = sqlite3.connect("database.sqlite")
connection.executescript(schema)
print("executed schema")

connection.close()
