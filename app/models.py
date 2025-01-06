from sqlalchemy import Column, String, Float
from geoalchemy2 import Geometry
from app.database import Base

class Parcel(Base):
    __tablename__ = "parcels"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    owner = Column(String, index=True)
    geometry = Column(Geometry("POLYGON", srid=4326))