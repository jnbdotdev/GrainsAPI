from sqlalchemy.orm import Session
from app.models import Parcel
from app.schemas import ParcelCreate, ParcelOut
from sqlalchemy import func
from geoalchemy2 import WKTElement
import uuid

# Função para criar uma nova parcela
def create_parcel(db: Session, parcel: ParcelCreate):
    db_parcel = Parcel(
        id=str(uuid.uuid4()),
        name=parcel.name,
        owner=parcel.owner,
        geometry=parcel.geometry
    )
    db.add(db_parcel)
    db.commit()
    db.refresh(db_parcel)

    # Agora vamos calcular a área da parcela
    area = db.query(func.ST_Area(db_parcel.geometry)).scalar()

    # Retorna a parcela com a área calculada
    return ParcelOut(
        id=db_parcel.id,
        name=db_parcel.name,
        owner=db_parcel.owner,
        area=area
    )


# Função para listar parcelas com filtro por bbox
def get_parcels_by_bbox(db: Session, minx: float, miny: float, maxx: float, maxy: float):
    # Definir a geometria do bounding box como um POLYGON no formato WKT (Well Known Text)
    bbox = f"POLYGON(({minx} {miny}, {maxx} {miny}, {maxx} {maxy}, {minx} {maxy}, {minx} {miny}))"

    # Converter para um WKTElement e definir o SRID correto
    bbox_geom = WKTElement(bbox, srid=4326)

    # Atualize para incluir a área na consulta
    parcels = db.query(
        Parcel.id,
        Parcel.name,
        Parcel.owner,
        func.ST_Area(Parcel.geometry).label("area")  # Calcular a área
    ).filter(
        Parcel.geometry.ST_Intersects(bbox_geom)  # Filtro por interseção do bbox
    ).all()

    # Agora, o resultado da consulta 'parcels' é uma lista de tuplas
    # Transforme cada tupla em um ParcelOut
    return [
        ParcelOut(
            id=parcel.id,
            name=parcel.name,
            owner=parcel.owner,
            area=parcel.area  # A área já foi calculada pela consulta
        )
        for parcel in parcels
    ]


