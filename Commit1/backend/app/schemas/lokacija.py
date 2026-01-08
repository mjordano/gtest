"""
Pydantic šeme za Lokacija (Location)
"""
from typing import Optional
from pydantic import BaseModel, Field


class LokacijaBase(BaseModel):
    """Bazna šema za lokaciju"""
    naziv: str = Field(..., min_length=1, max_length=200)
    opis: Optional[str] = None
    g_sirina: Optional[float] = Field(None, ge=-90, le=90)
    g_duzina: Optional[float] = Field(None, ge=-180, le=180)
    adresa: str = Field(..., min_length=1, max_length=300)
    grad: str = Field(..., min_length=1, max_length=100)


class LokacijaCreate(LokacijaBase):
    """Šema za kreiranje lokacije"""
    pass


class LokacijaUpdate(BaseModel):
    """Šema za ažuriranje lokacije"""
    naziv: Optional[str] = Field(None, min_length=1, max_length=200)
    opis: Optional[str] = None
    g_sirina: Optional[float] = Field(None, ge=-90, le=90)
    g_duzina: Optional[float] = Field(None, ge=-180, le=180)
    adresa: Optional[str] = Field(None, min_length=1, max_length=300)
    grad: Optional[str] = Field(None, min_length=1, max_length=100)


class LokacijaResponse(LokacijaBase):
    """Šema za odgovor sa podacima lokacije"""
    id_lokacija: int
    
    class Config:
        from_attributes = True
