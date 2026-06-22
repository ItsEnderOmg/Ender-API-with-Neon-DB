from fastapi import FastAPI, HTTPException, Depends # Lo que usa la API
from fastapi.middleware.cors import CORSMiddleware #N omas pa permitir ciertas solicitudes
from database import Base, engine, SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated, List
import models
import schemas
app = FastAPI()

Base.metadata.create_all(bind=engine)

# Configurar CORS para permitir solicitudes desde cualquier origen
app.add_middleware(
    CORSMiddleware,
    # allow_origins=["*"],  # Permite todos los orígenes
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, DELETE, etc)
    allow_headers=["*"],  # Permite todos los headers
)

def get_db(): 
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()

# @app.get("/users/{user_id}")
# async def get_users_by_id(user_id : int, db: Session = Depends(get_db)):
#     #user = db.query(models.User).filter(schemas.User.id == user_id).first
#     pass


@app.get("/")
async def root():
    return {"message": "Gyaru"}

# response_model hace que return muestre solo las instancias de ese objeto (de la base de datos)
# que se llamen igual que las instancias de la clase que creamos en schemas
@app.post("/users/create_user", response_model = schemas.UserResponse)
# "user" sera un objeto de clase UserCreate (como lo creamos con BaseModel tiene validacion de datos)
async def create_user(user : schemas.UserCreate ,db: Session = Depends(get_db)):
    # User es un objeto de una tabla creada en models
    new_user = models.User(
        # username,email,password son los nombres de las columnas en la tabla
        # les asignamos las los valores de instancia de la clase UserCreate q ingreso el cliente
        username = user.username,
        email = user.email,
        password = user.password
    )
    # Agrega el usuario y retorna datos segun response_model 
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Esto de aqui esta mal, lo hariamos asi si no hubieramos definido una clase para retornar valores 
    # especificos en response_model, por eso es tan importante, para no escribir cada vez
    # Cuales valores deberiamos devolver 
    return {"id" : new_user.id, "username" : new_user.username, "email" : new_user.email}

@app.get("/users/get_user_by_id/{id}", response_model = schemas.UserResponse)
async def get_user(id : int, db : Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if user:
        return user
    raise HTTPException(status_code=404, details="ID doesn't exist")

@app.get("/users/get_all_users")
async def get_all_users(db : Session = Depends(get_db)):
    result = db.query(models.User).all()
    return result