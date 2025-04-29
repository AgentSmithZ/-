import sqlite3

db = sqlite3.connect('database.db')

c = db.cursor()

c.execute("""CREATE TABLE users (
      nickname text,
      password text,
      role_id integer
 )""")

c.execute("""CREATE TABLE roles (
      role text
  )""")

c.execute("INSERT INTO roles VALUES('Admin')")
c.execute("INSERT INTO roles VALUES('Waiter')")
c.execute("INSERT INTO roles VALUES('Cook')")

c.execute("INSERT INTO users VALUES('admin', '123456', '1')")
c.execute("INSERT INTO users VALUES('waiter', '654321', '2')")
c.execute("INSERT INTO users VALUES('cook', '321456', '3')")

# c.execute("DELETE FROM users")
# c.execute("DELETE FROM roles")

db.commit()


db.close()
