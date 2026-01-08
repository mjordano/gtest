"""
Pydantic šeme za Prijava (Registration)
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from app.schemas.izlozba import IzlozbaResponse


class PrijavaBase(BaseModel):
    """Bazna šema za prijavu"""
    id_izlozba: int
    broj_karata: int = Field(default=1, ge=1, le=10)


class PrijavaCreate(PrijavaBase):
    """Šema za kreiranje prijave"""
    pass


class PrijavaUpdate(BaseModel):
    """Šema za ažuriranje prijave"""
    broj_karata: Optional[int] = Field(None, ge=1, le=10)
    validirano: Optional[bool] = None


class PrijavaResponse(BaseModel):
    """Šema za odgovor sa podacima prijave"""
    id_prijava: int
    id_korisnik: int
    id_izlozba: int
    id_slika: Optional[int] = None
    broj_karata: int
    qr_kod: Optional[str] = None
    validirano: bool
    datum_registracije: datetime
    slika_qr: Optional[str] = None
    verifikovan_email: bool
    email_poslat: bool
    datum_slanja_emaila: Optional[datetime] = None
    izlozba: Optional[IzlozbaResponse] = None
    
    class Config:
        from_attributes = True


class PrijavaValidate(BaseModel):
    """Šema za validaciju QR koda"""
    qr_kod: str
