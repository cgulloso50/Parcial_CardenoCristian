"""RNF03 – Confiabilidad.

Medida: 0 excepciones no controladas ante 100 o más entradas inválidas a
elegir() y ante 10 archivos corruptos. Procedimiento reproducible: semilla
fija y archivos generados en un directorio temporal.
"""
import random
import string

import pytest

from motor.cargador import cargar_historia
from motor.errores import ErrorContenido, ErrorJugada
from motor.sesion import Sesion
from tests.conftest import RUTA_REAL

SEMILLA = 2026


def estado(s):
    return (s.escena_actual.id, s.variables, s.puede_deshacer())


def intentar_invalido(s, entrada):
    """La entrada debe rechazarse con ErrorJugada y dejar la sesión intacta."""
    antes = estado(s)
    with pytest.raises(ErrorJugada):
        s.elegir(entrada)
    assert estado(s) == antes


def id_aleatorio(rng, prohibidos):
    alfabeto = string.ascii_letters + string.digits + "_- áéñ"
    while True:
        candidato = "".join(rng.choice(alfabeto) for _ in range(rng.randint(0, 12)))
        if candidato not in prohibidos:
            return candidato


def test_rnf03_mas_de_100_entradas_invalidas_no_producen_excepciones_no_controladas():
    rng = random.Random(SEMILLA)
    historia = cargar_historia(RUTA_REAL)
    ids_validos = {o.id for e in historia.escenas.values() for o in e.opciones}
    s = Sesion(historia)
    intentos = 0

    # Fase 1: escena inicial, sin historial
    fase1 = [None, 123, "", " ", "E2", "activar_codigo", "investigar"]
    fase1 += [id_aleatorio(rng, ids_validos) for _ in range(50)]
    for entrada in fase1:
        intentar_invalido(s, entrada)
        intentos += 1
    assert not s.puede_deshacer()

    # Fase 2: E3 sin conocer el origen (activar_codigo existe pero no está habilitada)
    s.elegir("revisar")
    s.elegir("continuar")
    assert s.escena_actual.id == "E3" and s.variables["conoce_origen"] is False
    fase2 = ["activar_codigo", "revisar", "investigar", None, ""]
    fase2 += [id_aleatorio(rng, ids_validos) for _ in range(50)]
    for entrada in fase2:
        intentar_invalido(s, entrada)
        intentos += 1

    assert intentos >= 100
    # Ninguna entrada inválida sustituyó el historial de la última elección válida
    assert s.puede_deshacer()
    s.deshacer()
    assert s.escena_actual.id == "E2"


ARCHIVOS_CORRUPTOS = [
    ("vacio", b""),
    ("llave_sin_cerrar", b"{"),
    ("null", b"null"),
    ("lista", b"[1, 2, 3]"),
    ("numero", b"123"),
    ("texto", b'"hola"'),
    ("objeto_vacio", b"{}"),
    ("bytes_invalidos", b"\xff\xfe\x00\x01"),
    ("escenas_no_es_lista",
     b'{"titulo":"x","inicio":"A","variables":{},"escenas":"no"}'),
    ("escenas_con_basura",
     b'{"titulo":"x","inicio":"A","variables":{},"escenas":[1,2]}'),
]


@pytest.mark.parametrize("nombre, contenido", ARCHIVOS_CORRUPTOS,
                         ids=[n for n, _ in ARCHIVOS_CORRUPTOS])
def test_rnf03_archivo_corrupto_se_rechaza_de_forma_controlada(tmp_path, nombre, contenido):
    ruta = tmp_path / f"{nombre}.json"
    ruta.write_bytes(contenido)
    with pytest.raises(ErrorContenido) as exc:
        cargar_historia(ruta)
    assert exc.value.errores
    assert all(isinstance(m, str) and m for m in exc.value.errores)