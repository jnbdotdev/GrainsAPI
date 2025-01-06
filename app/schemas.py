from pydantic import BaseModel

class ParcelCreate(BaseModel):
    name: str
    owner: str
    geometry: str

class ParcelOut(BaseModel):
    id: str
    name: str
    owner: str
    area: float

    class Config:
        from_attributes = True