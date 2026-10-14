import pytest

from motor.cargador import cargar_historia
from motor.sesion import Sesion
from tests.conftest import RUTA_REAL

RUTA_SEGUNDA = RUTA_REAL.parent / "segunda_historia.json"


def ids(sesion):
    return [o.id for o in sesion.opciones_disponibles()]


def test_segunda_historia_carga_con_el_mismo_motor():
    historia = cargar_historia(RUTA_SEGUNDA)
    assert historia.titulo == "El faro apagado"
    assert len(historia.escenas) >= 3


@pytest.mark.parametrize("primera, esperada, destino_final", [
    ("encender", "subir_con_luz", "F3"),
    ("entrar_oscuras", "subir_a_oscuras", "F4"),
])
def test_condicion_cambia_las_opciones_y_el_final(primera, esperada, destino_final):
    s = Sesion(cargar_historia(RUTA_SEGUNDA))
    s.elegir(primera)
    assert ids(s) == [esperada]            # la condición oculta la otra opción
    s.elegir(esperada)
    assert s.escena_actual.id == destino_final and s.esta_finalizada()


def test_deshacer_funciona_en_la_segunda_historia():
    s = Sesion(cargar_historia(RUTA_SEGUNDA))
    s.elegir("encender")
    assert s.variables["tiene_luz"] is True
    s.deshacer()
    assert s.escena_actual.id == "F1" and s.variables["tiene_luz"] is False