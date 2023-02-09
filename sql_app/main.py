from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
import crud
import models
import schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
usuarios=[]


# Dependency 
def get_db():
    db = SessionLocal() #nos manda DML
    try:
        yield db
    finally:
        db.close()


@app.post("/Crear_users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="correo electrónico ya registrado")
    return crud.create_user(db=db, user=user)


#RECOGE TODA LA INFORMACION DE LAS 2 TABLAS ENLAZADAS PK Y FK
@app.get("/Leer_users_items/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/Leer_users/", response_model=List[schemas.User_tb_todo])
def read_users(db: Session = Depends(get_db)):
    data=db.query(models.User).all()#tabla todo
    return data



@app.get("/Leer_ciertos_users/{user_id}", response_model=schemas.ShowUser)
def read_users(user_id: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    usuario=db.query(models.User).filter(models.User.id == user_id).first()#filtra y obtiene toda las columnas
    if not usuario:
      return{"RESPUESTA":"USUARIO NO ENCONTRADO.!"}
    return usuario #devuelve el filtro de columnas a mostrar ShowUser


#FILTRA LAS COLUMNAS QUE QUERRAMOS QUE SE MUESTRE EN SHOWUSER
@app.get("/Leer_ciertos_users/", response_model=List[schemas.ShowUser])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users	


@app.delete("/Eliminar_Usuario")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id)
    if not db_user.first(): #Devuelve el primer resultado de esta Consulta
       # return{"RESPUESTA: USUARIO NO ENCONTRADO.!!"}
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db_user.delete(synchronize_session=False)
    db.commit()
    return {"RESPUESTA: USUARIO ELIMINADO CORRECTO.!"}


#UN ACTUALIZAR DE MANERA TEMPORAL
# @app.put("/user/{user_id}")
# def actualizar_usuario(user_id:int,updateUser:schemas.UserCreate): #parametros
# 	for index,user in enumerate(usuarios):#recorrer los usuarios
# 		if user["id"]==user_id:#verificar si el id son iguales
# 			usuarios[index]["id"] = updateUser.dict["id"]
# 			usuarios[index]["email"] = updateUser.dict["email"]#encontrar el user correspondiente en ese index
# 			usuarios[index]["hashed_password"] = updateUser.dict["hashed_password"]
# 			usuarios[index]["is_active"] = updateUser.dict["is_active"]
# 			return{"RESPUESTA: USUARIO ACTUALIZADO CON ÈXITO.!"}
# 	return{"RESPUESTA: USUARIO NO ENCONTRADO .!"}		


@app.put("/user/{user_id}") #tmb utilza el path
def actualizar_usuario(user_id:int,updateUser:schemas.UserUpate,db: Session = Depends(get_db)): #parametros
	db_user = db.query(models.User).filter(models.User.id == user_id)#obtener el usuario 
	if not db_user.first():
		return{"RESPUESTA: USUARIO NO ENCONTRADO .!"}	
	db_user.update(updateUser.dict(exclude_unset=True))#convertir en diccionario,y solo actualize los que estan llegando
	db.commit()	
	
	return{"RESPUESTA: USUARIO ACTUALIZADO CON ÈXITO.!"}
		





#Leer por ID y recoger toda la fila de la otra tabla por su ID FK
@app.get("/Usuario/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_user


@app.post("/Leer_ID/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)):	
    return crud.create_user_item(db=db, item=item, user_id=user_id)



@app.get("/items/", response_model=List[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items

