import sqlite3

conn = sqlite3.connect("data_base.db")
c = conn.cursor()

c.execute("""
        SELECT * FROM table1  
          """)

print(len(list(row for row in c.fetchall())))

c.execute("""
        CREATE TABLE IF NOT EXISTS table1 (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user STRING UNIQUE,
        email STRING UNIQUE
      )
""")


conn.commit()
conn.close()

