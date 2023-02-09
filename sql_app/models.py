from sqlalchemy import Boolean, Column, ForeignKey, Integer, String ,DateTime
from sqlalchemy.orm import relationship

from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))
    is_active = Column(Boolean, default=True)
    #fecha=Column(DateTime,default=datetime.now,onupdate=datetime.now)
    items = relationship("Item", back_populates="owner") #UNO


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    description = Column(String(255), index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items") #MUCHOS ....Un usuario puede tener muchos Items
