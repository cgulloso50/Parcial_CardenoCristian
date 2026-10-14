import copy
from pathlib import Path

import pytest

from motor.cargador import construir_historia
from motor.sesion import Sesion

RUTA_REAL = Path(__file__).resolve().parent.parent / "historias" / "la_ultima_transmision.json"

_BASE = {
    "titulo": "Mini",
    "inicio": "A",
    "variables": {"llave": False},
    "escenas": [
        {"id": "A", "texto": "Inicio", "final": False, "opciones": [
            {"id": "tomar", "texto": "Tomar llave", "destino": "B",
             "condiciones": {}, "efectos": {"llave": True}},
            {"id": "abrir", "texto": "Abrir puerta", "destino": "C",
             "condiciones": {"llave": True}, "efectos": {}}]},
        {"id": "B", "texto": "Pasillo", "final": False, "opciones": [
            {"id": "volver", "texto": "Volver", "destino": "A",
             "condiciones": {}, "efectos": {}}]},
        {"id": "C", "texto": "Fin", "final": True, "opciones": []},
    ],
}


@pytest.fixture
def datos():
    return copy.deepcopy(_BASE)


@pytest.fixture
def sesion(datos):
    return Sesion(construir_historia(datos))