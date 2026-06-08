# Los type hints son para mejorar legibilidad y la experiencia al escribir el codigo.
# Python los ignora, son para los desarrolladores y de ayuda para que el editor de codigo detecte errores,
# sugiera codigo o autocomplete cosas.  (Aunque puedes importar modulos q si trabajan con los type)
#     return "Your full name is: " + first_name.title() + " " + second_name.capitalize() + str(age)

# print(full_name("jOSTIn", "Lenin", 17))

from fastapi import FastAPI, HTTPException
import sqlite3

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome to ender's API"}


@app.get("/usuarios")
def get_users():
    users = []

    with sqlite3.connect("data_base.db") as conn:
        c = conn.cursor()
        c.execute("SELECT rowid, nombre FROM table1")
        
        for row in c.fetchall():
            users.append({"id": row[0], "usuario": row[1]})

    return users

@app.get("/users_emails")       
def get_emails():
    emails = []

    with sqlite3.connect("data_base.db") as conn:
        c = conn.cursor()
        c.execute("SELECT rowid, nombre, correo_electronico FROM table1")
        for row in c.fetchall():
            emails.append({"id": row[0],
                            "usuario": row[1],
                            "email": row[2]})
    return emails

@app.delete("/personaje/{name}")
def delete_personaje(name: str):
    with sqlite3.connect("data_base.db") as conn:
        # conn.execute("PRAGMA foreign_keys = OFF")
        c = conn.cursor()

        # La "," es obligatoria para crear una tupla con un solo elemento
        c.execute("""
                DELETE FROM table1
                WHERE nombre = ?
                """, (name,))
        conn.commit()
    return {"mensaje": f"El personaje {name} se ha eliminado correctamente"}


@app.delete("/personaje/{id}")
def delete_personaje_by_id(id: int):
    
    if id >= 1:
        with sqlite3.connect("data_base.db") as conn:
            # conn.execute("PRAGMA foreign_keys = OFF")
            c = conn.cursor()
            c.execute("""
                    DELETE FROM table1 WHERE rowid = ?
                    """, (id,))
            conn.commit()
        return {"mensaje": f"El personaje con el id={id} se ha eliminado correctamente"}
    
    else:
        raise HTTPException(status_code= 400, detail="Integer 'id' needs to be greater than 0")

@app.delete("/delete_all")
def delete_all():
    with sqlite3.connect("data_base.db") as conn:
        # conn.execute("PRAGMA foreign_keys = OFF")
        c = conn.cursor()
        c.execute("DELETE FROM table1")        

        conn.commit()
    return {"mensaje": "Se elimino todo wow"}

@app.post("/new_user")
def create_new_user(username: str, email:str):
    with sqlite3.connect("data_base.db") as conn:
        c = conn.cursor()
        c.execute("""
                INSERT INTO table1 (user, email)
                VALUES (?,?)
            """, (username, email))
        conn.commit()
    return {"message": f"El usuario {username} se agrego correctamente."}
        

