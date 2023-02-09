from typing import List, Optional

from pydantic import BaseModel
from pydantic import Field

class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):#HERENCIA al final imprime email y password
    password: str


class UserUpate(BaseModel):
	id: int =None
	email: str =None
	hashed_password: str =None
	is_active: bool =None


class User_tb(BaseModel):
	id: int
	email: str
	hashed_password: str
	is_active: bool
	class Config: #muy importante por que la tabla user tiene mas columnas no importa si lleva PK y FK siempre se pone
		orm_mode = True

class User_tb_todo(User_tb):
    pass


class UserDelete(UserBase):
    id: int = Field(
		example="5"
	) #proporcionar información adicional sobre un campo



#LLAMAR SOLO ALGUNAS COLUMNAS DE LA TABLA
class User(UserBase):
    id: int
    is_active: bool
    items: List[Item] = [] #trae datos de la clase
    #A QUE ORM SE TIENE QUE INSTANCIAR
    class Config:
        orm_mode = True


#LLAMAR SOLO ALGUNAS COLUMNAS DE LA TABLA
class ShowUser(BaseModel):
	email:str
	#A QUE ORM SE TIENE QUE INSTANCIAR
	class Config():
		orm_mode=True
