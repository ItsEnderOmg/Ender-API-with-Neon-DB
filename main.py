from fastapi import FastAPI, HTTPException, Depends # Lo que usa la API
from fastapi.middleware.cors import CORSMiddleware #N omas pa permitir ciertas solicitudes
from database import Base, engine, SessionLocal
from sqlalchemy.orm import Session
import models
import schemas

app = FastAPI()

Base.metadata.create_all(bind=engine)

# Configurar CORS para permitir solicitudes desde cualquier origen
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],  # Permite todos los orígenes
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, DELETE, etc)
    allow_headers=["*"],  # Permite todos los headers
)

#Esto es la coneccion practicamente
def get_db(): 
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()

@app.get("/")
async def root():
    return {"message": "Gyaru"}

# Read User by id and only returns the values you specified in UserResponse
@app.get("/users/{id}", response_model = schemas.UserResponse)
async def get_users_by_id(id : int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if user:
        return user
    raise HTTPException(status_code=404, detail="User not found.")

#Read all users 
@app.get("/users", response_model = list[schemas.UserResponse])
async def get_all_users(db : Session = Depends(get_db)):
    all_users = db.query(models.User).all()
    if all_users:
        return all_users
    raise HTTPException(status_code=404, detail="What?! There's nothing in the database...")

#Count how many users are in the database
@app.get("/users/count")
async def count_users(db : Session = Depends(get_db)):
    return db.query(models.User).count()

# response_model hace que return muestre solo las instancias de ese objeto (de la base de datos)
# que se llamen igual que las instancias de la clase que creamos en schemas
@app.post("/users", response_model = schemas.UserResponse)
# "user" sera un objeto de clase UserCreate (como lo creamos con BaseModel tiene validacion de datos)
async def create_user(user : schemas.UserCreate, db: Session = Depends(get_db)):
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

#Delete a user from the database
@app.delete("/users/{id}")
async def delete_user(id : int, db : Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User ID not found")
    db.delete(user)
    db.commit()
    return {"message": f"The user with id = {id} was deleted."} 

#Update a value of a user in the db (the values are optional, the client doesnt need to update everything)
@app.patch("/users/{id}", response_model=schemas.UserResponse)
async def update_user(user_id: int, new_user_data: schemas.UserUpdate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code = 404, detail= f"User with id={user_id} does not exist.")

    # This converts the json (new_user_data, aka the data the client sent) to a dict, but exclude_unset=True only includes de keys with values =! None
    data_to_update = new_user_data.model_dump(exclude_unset=True)

    # Iterates the dict with the data the cllient sent and pdates the user.key with the new value/s
    for key, value in data_to_update.items():
        setattr (user , key, value)
    
    db.commit()
    db.refresh(user)
    return user

# It's like the last function but you use the class UserCreate for the data the client needs to send (bc every data is needed)
@app.put("/users/{user_id}", response_model=schemas.UserResponse)
async def update_whole_user(user_id: int, new_user_data: schemas.UserCreate, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User does not exist.")
    
    # You have to change the data manually
    user.username = new_user_data.username
    user.email = new_user_data.email
    user.password = new_user_data.password

    db.commit()
    db.refresh(user)
    return user
