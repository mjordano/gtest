"""
Glavna FastAPI aplikacija
Sistem za upravljanje izložbama fotografija
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.config import settings
from app.database import engine, Base
from app.routers import auth, korisnici, lokacije, izlozbe, slike, prijave

# Konfigurisanje logging-a
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifecycle manager za aplikaciju.
    Izvršava se pri pokretanju i gašenju.
    """
    # Startup
    logger.info("Pokretanje aplikacije...")
    
    # Kreiranje tabela (za development)
    # U produkciji koristiti Alembic migracije
    Base.metadata.create_all(bind=engine)
    logger.info("Baza podataka inicijalizovana")
    
    yield
    
    # Shutdown
    logger.info("Gašenje aplikacije...")


# Kreiranje FastAPI instance
app = FastAPI(
    title="Galerija Izložbi API",
    description="""
    ## API za upravljanje izložbama fotografija
    
    ### Funkcionalnosti:
    * 🔐 **Autentifikacija** - JWT bazirana prijava i registracija
    * 👥 **Korisnici** - Upravljanje korisničkim nalozima
    * 📍 **Lokacije** - Galerije i prostori za izložbe
    * 🖼️ **Izložbe** - Kreiranje i upravljanje izložbama
    * 📸 **Slike** - Fotografije sa Art Institute of Chicago API
    * 🎫 **Prijave** - Rezervacija karata sa QR kodovima
    
    ### Tipovi korisnika:
    * **Običan korisnik** - Pregled izložbi i prijava
    * **Osoblje** - Upravljanje sadržajem
    * **Administrator** - Pun pristup sistemu
    """,
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registracija ruta
app.include_router(auth.router)
app.include_router(korisnici.router)
app.include_router(lokacije.router)
app.include_router(izlozbe.router)
app.include_router(slike.router)
app.include_router(prijave.router)


@app.get("/", tags=["Root"])
async def root():
    """
    Početna ruta - informacije o API-ju.
    """
    return {
        "message": "Dobrodošli u Galerija Izložbi API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint za monitoring.
    """
    return {"status": "healthy"}
