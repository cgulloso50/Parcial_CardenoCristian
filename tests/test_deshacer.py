import pytest

from motor.cargador import cargar_historia, construir_historia
from motor.errores import ErrorJugada
from motor.sesion import Sesion
from tests.conftest import RUTA_REAL


def estado(s):
    return (s.escena_actual.id, s.variables)


@pytest.fixture
def sesion_con_bloqueada(datos):
    """Historia mínima con una opción en B que solo se habilita sin llave."""
    datos["escenas"][1]["opciones"].append({
        "id": "bloqueada", "texto": "Solo sin llave", "destino": "C",
        "condiciones": {"llave": False}, "efectos": {}})
    return Sesion(construir_historia(datos))


# ---------------------------- U6 ----------------------------

def test_u6_deshacer_restaura_escena_y_variables_y_consume_retroceso(sesion):
    inicial = estado(sesion)
    sesion.elegir("tomar")
    assert sesion.variables["llave"] is True
    sesion.deshacer()
    assert estado(sesion) == inicial
    assert not sesion.puede_deshacer()
    with pytest.raises(ErrorJugada):       # segundo intento: no cambia nada
        sesion.deshacer()
    assert estado(sesion) == inicial


@pytest.mark.parametrize("id_invalido", ["no_existe", "bloqueada"])
def test_u6_entrada_invalida_preserva_el_historial(sesion_con_bloqueada, id_invalido):
    s = sesion_con_bloqueada
    s.elegir("tomar")                      # A -> B, llave = True
    antes = estado(s)
    with pytest.raises(ErrorJugada):
        s.elegir(id_invalido)
    assert estado(s) == antes
    assert s.puede_deshacer()
    s.deshacer()
    assert estado(s) == ("A", {"llave": False})


def test_u6_nueva_eleccion_vuelve_a_habilitar_el_retroceso(sesion):
    sesion.elegir("tomar")
    sesion.deshacer()
    assert not sesion.puede_deshacer()
    sesion.elegir("tomar")
    assert sesion.puede_deshacer()


def test_u6_deshacer_solo_revierte_la_ultima_eleccion(sesion):
    sesion.elegir("tomar")                 # A -> B (llave = True)
    sesion.elegir("volver")                # B -> A
    sesion.deshacer()
    assert estado(sesion) == ("B", {"llave": True})
    assert not sesion.puede_deshacer()


def test_u6_no_hay_retroceso_al_iniciar(sesion):
    assert not sesion.puede_deshacer()
    with pytest.raises(ErrorJugada):
        sesion.deshacer()
    assert estado(sesion) == ("A", {"llave": False})


def test_u6_deshacer_desde_un_final(sesion):
    sesion.elegir("tomar")
    sesion.elegir("volver")
    sesion.elegir("abrir")                 # A -> C (final)
    assert sesion.esta_finalizada()
    sesion.deshacer()
    assert estado(sesion) == ("A", {"llave": True})


# ------------------------ U5 extendida ------------------------

def test_u5_reiniciar_elimina_el_historial(sesion):
    sesion.elegir("tomar")
    sesion.reiniciar()
    assert estado(sesion) == ("A", {"llave": False})
    assert not sesion.puede_deshacer()
    with pytest.raises(ErrorJugada):
        sesion.deshacer()


# ------------------------ I1 extendida ------------------------

def test_i1_deshacer_desde_un_final_con_archivo_real():
    s = Sesion(cargar_historia(RUTA_REAL))
    for id_opcion in ("revisar", "investigar", "activar_codigo"):
        s.elegir(id_opcion)
    assert s.escena_actual.id == "E4" and s.esta_finalizada()
    assert s.variables == {"conoce_origen": True, "confia_en_la_voz": True}
    s.deshacer()
    assert s.escena_actual.id == "E3"
    assert s.variables == {"conoce_origen": True, "confia_en_la_voz": False}


def test_i1_ejemplo_del_anexo_de_la_hora_6():
    s = Sesion(cargar_historia(RUTA_REAL))
    s.elegir("revisar")
    s.elegir("investigar")
    assert s.escena_actual.id == "E3" and s.variables["conoce_origen"] is True
    s.deshacer()
    assert s.escena_actual.id == "E2" and s.variables["conoce_origen"] is False
    with pytest.raises(ErrorJugada):
        s.deshacer()
    assert s.escena_actual.id == "E2"
    s.elegir("continuar")
    assert sorted(o.id for o in s.opciones_disponibles()) == ["activar_sin_verificar", "cortar"]