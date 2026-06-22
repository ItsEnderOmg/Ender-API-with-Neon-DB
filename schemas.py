from pydantic import BaseModel, Field, EmailStr

#Validacion de los datos que ingresan pa crear un usuario
class UserCreate(BaseModel):
    username : str = Field(pattern=r"[a-zA-Z-0-9_]{3,20}$")
    password : str
    email : EmailStr

#Esto es pa controlar las info que devuelves sobre los usuarios xd
class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    #Esto es pa q permita leer datos desde un objeto SQLAlchemy
    class Config:
        from_attributes = True