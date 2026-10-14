import copy

import pytest

from motor.cargador import cargar_historia, construir_historia
from motor.errores import ErrorContenido


def _inicio(d): d["inicio"] = "X9"
def _escena_dup(d): d["escenas"].append(copy.deepcopy(d["escenas"][0]))
def _opcion_dup(d): d["escenas"][0]["opciones"].append(copy.deepcopy(d["escenas"][0]["opciones"][0]))
def _destino(d): d["escenas"][0]["opciones"][0]["destino"] = "E99"
def _var_condicion(d): d["escenas"][0]["opciones"][1]["condiciones"] = {"fantasma": True}
def _var_efecto(d): d["escenas"][0]["opciones"][0]["efectos"] = {"fantasma": True}
def _no_booleano(d): d["escenas"][0]["opciones"][0]["efectos"] = {"llave": "si"}
def _falta_campo(d): del d["titulo"]
def _final_con_opciones(d): d["escenas"][2]["opciones"] = copy.deepcopy(d["escenas"][0]["opciones"][:1])
def _nofinal_sin_opciones(d): d["escenas"][1]["opciones"] = []

CASOS = [
    (_inicio, "'X9' no existe"),
    (_escena_dup, "ID de escena duplicado: 'A'"),
    (_opcion_dup, "ID de opción duplicado 'tomar'"),
    (_destino, "'E99' no existe"),
    (_var_condicion, "'fantasma' no está declarada"),
    (_var_efecto, "'fantasma' no está declarada"),
    (_no_booleano, "no es booleano"),
    (_falta_campo, "falta el campo obligatorio 'titulo'"),
    (_final_con_opciones, "Escena 'C': es final"),
    (_nofinal_sin_opciones, "Escena 'B': no es final"),
]


@pytest.mark.parametrize("mutar, fragmento", CASOS)
def test_u4_errores_de_contenido_son_rechazados_con_mensaje(datos, mutar, fragmento):
    mutar(datos)
    with pytest.raises(ErrorContenido) as exc:
        construir_historia(datos)
    assert fragmento in "\n".join(exc.value.errores)


def test_u4_archivo_inexistente(tmp_path):
    with pytest.raises(ErrorContenido) as exc:
        cargar_historia(tmp_path / "nada.json")
    assert "no se encontró" in exc.value.errores[0]


def test_u4_archivo_ilegible(tmp_path):
    f = tmp_path / "roto.json"
    f.write_text("{esto no es json", encoding="utf-8")
    with pytest.raises(ErrorContenido) as exc:
        cargar_historia(f)
    assert "no es un JSON legible" in exc.value.errores[0]


def test_u4_estructura_incorrecta(tmp_path):
    f = tmp_path / "lista.json"
    f.write_text("[1, 2, 3]", encoding="utf-8")
    with pytest.raises(ErrorContenido):
        cargar_historia(f)
