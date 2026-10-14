import pytest

from motor.cargador import construir_historia
from motor.errores import ErrorJugada
from motor.sesion import Sesion


def ids(sesion):
    return [o.id for o in sesion.opciones_disponibles()]


def test_u1_condiciones_habilitan_solo_las_correspondientes(sesion):
    assert ids(sesion) == ["tomar"]            # llave=False: "abrir" oculta
    sesion.elegir("tomar")
    sesion.elegir("volver")
    assert ids(sesion) == ["tomar", "abrir"]   # llave=True: aparece "abrir"


def test_u2_eleccion_valida_aplica_efectos_y_avanza(sesion):
    sesion.elegir("tomar")
    assert sesion.escena_actual.id == "B"
    assert sesion.variables["llave"] is True


@pytest.mark.parametrize("id_opcion", ["abrir", "no_existe"])
def test_u3_opcion_invalida_deja_estado_intacto(sesion, id_opcion):
    antes = (sesion.escena_actual.id, sesion.variables)
    with pytest.raises(ErrorJugada):
        sesion.elegir(id_opcion)
    assert (sesion.escena_actual.id, sesion.variables) == antes


def test_u5_reiniciar_restaura_estado_inicial(sesion):
    sesion.elegir("tomar")
    sesion.reiniciar()
    assert sesion.escena_actual.id == "A"
    assert sesion.variables == {"llave": False}


def test_final_se_reconoce(sesion):
    sesion.elegir("tomar"); sesion.elegir("volver"); sesion.elegir("abrir")
    assert sesion.esta_finalizada() and not sesion.esta_bloqueada()


def test_bloqueo_en_escena_no_final_sin_opciones_habilitadas(datos):
    datos["escenas"][0]["opciones"] = [datos["escenas"][0]["opciones"][1]]  # solo "abrir"
    sesion = Sesion(construir_historia(datos))
    assert sesion.opciones_disponibles() == []
    assert sesion.esta_bloqueada()
    sesion.reiniciar()
    assert sesion.escena_actual.id == "A"
