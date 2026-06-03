# Los type hints son para mejorar legibilidad y la experiencia al escribir el codigo.
# Python los ignora, son para los desarrolladores y de ayuda para que el editor de codigo detecte errores,
# sugiera codigo o autocomplete cosas.  (Aunque puedes importar modulos q si trabajan con los type)
#     return "Your full name is: " + first_name.title() + " " + second_name.capitalize() + str(age)

# print(full_name("jOSTIn", "Lenin", 17))

from fastapi import FastAPI
import sqlite3

app = FastAPI()

@app.get("/usuarios")
def get_users():
    conn = sqlite3.connect("data_base.db")
    c = conn.cursor()
    c.execute("SELECT rowid, usuario FROM usuarios")
    
    users = []
    for row in c.fetchall():
        users.append({"id": row[0], "usuario": row[1]})
    conn.close
    return users       
    



