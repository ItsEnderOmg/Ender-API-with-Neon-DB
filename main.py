from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
from pydantic import BaseModel, Field

app = FastAPI()

# Configurar CORS para permitir solicitudes desde cualquier origen
app.add_middleware(
    CORSMiddleware,
    # allow_origins=["*"],  # Permite todos los orígenes
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, DELETE, etc)
    allow_headers=["*"],  # Permite todos los headers
)
# DATABASE_URL = "postgesql://ender:2009@localhost:5432/my_db"
# engine = create_engine(DATABASE_URL)

# Aqui nomas creo un usuario de la forma tradicional pa practicar xddd
# class User:
#     def __init__(self, username:str, password:str, email:str, phone: int):
#         self.username = username
#         self.password = password
#         self.email = email
#         self.phone - phone


class User(BaseModel):
    username : str = Field(pattern=r"[a-zA-Z-0-9_]{3,20}$")
    age : int = Field(ge=18, le=60)

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


# Si solo ponias "personaje/{name}" daba errores por fixed paths pq luego usabas la misma ruta con otro parametro
@app.delete("/personaje/name/{name}")
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


@app.delete("/personaje/id/{id}")
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
    return {"mensaje": "Se elimino todo wow por que lo hiciste?XDXDXD"}

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
        

