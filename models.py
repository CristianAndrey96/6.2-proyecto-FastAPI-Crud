from sqlalchemy import Column, Integer, String
from database import Base

class CarroBD(Base):
    __tablename__ = 'carros'

    id = Column(String, primary_key=True, index=True)
    marca = Column(String, index=True)
    modelo = Column(Integer)