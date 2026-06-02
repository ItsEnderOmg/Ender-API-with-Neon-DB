#Imports the SQLite module
import sqlite3

#Connects to the database and creates it if doesnt exist
connection = sqlite3.connect("data_base.db")

#Here you create the cursor, and call it however you want
c = connection.cursor()

#Creating a table with columns
c.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          usuario TEXT,
          email TEXT,
          phone INTEGER,
   TEXT         
    )""")

c.execute("""
        CREATE TABLE IF NOT EXISTS devil_fruits (
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           Name TEXT,
           Type TEXT,
           Ownner TEXT,
           Description TEXT
    )""")

# user_name = input("Insert your username: ")
# user_email = input("Insert your email: ")
# user_phone = input("Insert your phone: ")
# user_data = [user_name, user_email, user_phone]

prueba = ["Shanks", None]

# c.execute("""
#         INSERT INTO usuarios (usuario, email)
#         VALUES (?,?)
# """, prueba)

c.execute("SELECT * FROM usuarios")


c.execute("""
        DELETE FROM usuarios
        WHERE rowid = 10

""")

c.execute("""
        CREATE TABLE IF NOT EXISTS nueva_tabla (
        nombre TEXT,
        correo_electronico TEXT
    )""")

c.execute("""
        INSERT INTO nueva_tabla(nombre, correo_electronico)
        SELECT usuario, phone FROM usuarios
""")

print(c.fetchall())

#Save the changes to the database
connection.commit()

#Closing the connection with the database
connection.close()


