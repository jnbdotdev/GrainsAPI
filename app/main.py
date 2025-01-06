import uuid

from fastapi import FastAPI, Depends, HTTPException
from geoalchemy2 import WKTElement
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.crud import get_parcels_by_bbox, create_parcel as create_new_parcel
from app.models import Parcel
from app.schemas import ParcelOut, ParcelCreate
from app.database import Base, engine, SessionLocal

app = FastAPI()

# Criação das tabelas no banco de dados
Base.metadata.create_all(bind=engine)

# Dependency para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint para criar uma parcela
@app.post("/parcels", response_model=ParcelOut)
def create_parcel(parcel: ParcelCreate, db: Session = Depends(get_db)):
    return create_new_parcel(db, parcel)


@app.post("/process/union")
def union_parcels(bbox: str, db: Session = Depends(get_db)):
    minx, miny, maxx, maxy = map(float, bbox.split(","))

    # Consulta as parcelas dentro do bounding box
    parcels = get_parcels_by_bbox(db, minx, miny, maxx, maxy)
    if not parcels:
        raise HTTPException(status_code=404, detail="Nenhuma parcela encontrada.")

    # Cria um polígono unificado com as parcelas selecionadas
    polygon_wkt = f"POLYGON(({minx} {miny}, {maxx} {miny}, {maxx} {maxy}, {minx} {maxy}, {minx} {miny}))"
    union_polygon = db.query(
        func.ST_Union(Parcel.geometry)
    ).filter(
        Parcel.geometry.ST_Intersects(WKTElement(polygon_wkt, srid=4326))
    ).scalar()

    # Salva o novo polígono unificado no banco de dados
    new_parcel = Parcel(
        id=str(uuid.uuid4()),
        name="Union Result",
        owner="System",
        geometry=union_polygon
    )
    db.add(new_parcel)
    db.commit()
    db.refresh(new_parcel)

    return new_parcel


# Endpoint para consultar parcelas por bounding box
@app.get("/parcels", response_model=list[ParcelOut])
def get_parcels(
        minx: float = -100,
        miny: float = -100,
        maxx: float = 100,
        maxy: float = 100,
        db: Session = Depends(get_db)
) -> list[ParcelOut]:
    if None in [minx, miny, maxx, maxy]:
        raise HTTPException(status_code=400, detail="Parâmetros de bounding box não fornecidos.")

    parcels = get_parcels_by_bbox(db, minx, miny, maxx, maxy)
    if not parcels:
        raise HTTPException(status_code=404, detail="Nenhuma parcela encontrada.")
    return parcels
