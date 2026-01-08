"""
QR kod servis
Generisanje QR kodova za prijave na izložbe
"""
import qrcode
import json
import base64
from io import BytesIO
from datetime import datetime
from typing import Dict, Any


def generate_qr_data(
    prijava_id: int,
    korisnik_id: int,
    izlozba_id: int,
    broj_karata: int
) -> str:
    """
    Generiše JSON string sa podacima za QR kod.
    
    Args:
        prijava_id: ID prijave
        korisnik_id: ID korisnika
        izlozba_id: ID izložbe
        broj_karata: Broj rezervisanih karata
        
    Returns:
        JSON string sa podacima prijave
    """
    data = {
        "prijava_id": prijava_id,
        "korisnik_id": korisnik_id,
        "izlozba_id": izlozba_id,
        "broj_karata": broj_karata,
        "datum_generisanja": datetime.utcnow().isoformat(),
        "verzija": "1.0"
    }
    return json.dumps(data)


def generate_qr_code(
    prijava_id: int,
    korisnik_id: int,
    izlozba_id: int,
    broj_karata: int
) -> Dict[str, str]:
    """
    Generiše QR kod za prijavu i vraća base64 encoded sliku.
    
    Args:
        prijava_id: ID prijave
        korisnik_id: ID korisnika
        izlozba_id: ID izložbe
        broj_karata: Broj rezervisanih karata
        
    Returns:
        Dict sa 'qr_data' (JSON string) i 'qr_image' (base64 string)
    """
    # Generisanje podataka za QR kod
    qr_data = generate_qr_data(prijava_id, korisnik_id, izlozba_id, broj_karata)
    
    # Kreiranje QR koda
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)
    
    # Generisanje slike (crno-beli dizajn)
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Konvertovanje u base64
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    
    return {
        "qr_data": qr_data,
        "qr_image": f"data:image/png;base64,{img_base64}"
    }


def decode_qr_data(qr_data: str) -> Dict[str, Any]:
    """
    Dekoduje podatke iz QR koda.
    
    Args:
        qr_data: JSON string iz QR koda
        
    Returns:
        Dict sa podacima prijave
        
    Raises:
        ValueError: Ako je format QR koda neispravan
    """
    try:
        data = json.loads(qr_data)
        required_fields = ["prijava_id", "korisnik_id", "izlozba_id"]
        
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Nedostaje polje: {field}")
        
        return data
    except json.JSONDecodeError:
        raise ValueError("Neispravan format QR koda")
