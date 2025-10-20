from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from starlette import status

from database import SessionLocal, engine
import models

#Crea las tablas en la base de datos si no existen
models.Base.metadata.create_all(bind=engine)

#Dependencia para obtener sesion de base datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Modelo de datos de los carros utilizando pydantic
class Carro(BaseModel):
    id: str
    marca: str
    modelo: int

    class Config:
        orm_mode = True

#Datos simulados
carros = [
    Carro(id="1", marca="mazda", modelo=1983),
    Carro(id="2", marca="honda", modelo=1993),
]

#Crear la app Fast API
app = FastAPI()
templates = Jinja2Templates(directory="templates")
#Servir archivos estaticos
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

#Obtener lista de carros
#@app.get("/carros", response_model=List[Carro])
#def get_carros(db: Session = Depends(get_db)):
#    return db.query(models.CarroBD).all()
@app.get("/carros",response_model=List[Carro])
def get_carros(db:Session=Depends(get_db)):
    try:
        data = db.query(models.CarroBD).all()
        print("Carros encontrados:", data)
        return data
    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail=str(e))
    
#Crear un carro
@app.post("/carros", status_code=status.HTTP_201_CREATED)
def create_carro(carro: Carro, db: Session = Depends(get_db)):
    db_carro = models.CarroBD(**carro.dict())
    db.add(db_carro)
    db.commit()
    db.refresh(db_carro)
    return {"message": "Created Car"}

#Eliminar un carro
@app.delete("/carros/{id}")
def delete_carro(id: str, db: Session = Depends(get_db)):
    carro = db.query(models.CarroBD).filter(models.CarroBD.id == id).first()
    if not carro:
        raise HTTPException(status_code=404, detail="Carro not found")
    db.delete(carro)
    db.commit()
    return {"message": "Deleted Car"}

#Actualizar un carro
@app.put("/carros/{id}")
def update_carro(id: str, carro: Carro, db: Session = Depends(get_db)):
    carro_db = db.query(models.CarroBD).filter(models.CarroBD.id == id).first()
    if not carro_db:
        raise HTTPException(status_code=404, detail="Carro not found")
    carro_db.marca = carro.marca
    carro_db.modelo = carro.modelo
    db.commit()
    return {"message": "Updated Car"}