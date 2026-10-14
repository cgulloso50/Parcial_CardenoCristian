import json

import pytest

from motor.cargador import cargar_historia
from motor.errores import ErrorContenido, ErrorJugada
from motor.sesion import Sesion
from tests.conftest import RUTA_REAL


def elegir_por_texto(sesion, texto):
    """Elige la opción habilitada cuyo texto empieza por 'texto'."""
    for o in sesion.opciones_disponibles():
        if o.texto.lower().startswith(texto.lower()):
            sesion.elegir(o.id)
            return
    raise AssertionError(f"No hay opción habilitada que empiece por '{texto}'")


def test_i1_archivo_real_hasta_un_final():
    sesion = Sesion(cargar_historia(RUTA_REAL))
    elegir_por_texto(sesion, "Revisar")
    elegir_por_texto(sesion, "Investigar")
    assert sesion.escena_actual.id == "E3" and sesion.variables["conoce_origen"] is True  # CA01
    textos = sorted(o.texto for o in sesion.opciones_disponibles())
    assert len(textos) == 2
    elegir_por_texto(sesion, "Activar con código")
    assert sesion.escena_actual.id == "E4" and sesion.esta_finalizada()


def test_ca02_activar_con_codigo_no_se_puede_forzar():
    sesion = Sesion(cargar_historia(RUTA_REAL))
    elegir_por_texto(sesion, "Revisar")
    elegir_por_texto(sesion, "Continuar")
    id_con_codigo = next(o.id for o in sesion.escena_actual.opciones
                         if o.texto.lower().startswith("activar con código"))
    with pytest.raises(ErrorJugada):
        sesion.elegir(id_con_codigo)
    elegir_por_texto(sesion, "Activar sin verificar")
    assert sesion.escena_actual.id == "E5"


def test_ca03_destino_inexistente_rechaza_la_carga(tmp_path):
    datos = json.loads(RUTA_REAL.read_text(encoding="utf-8"))
    datos["escenas"][0]["opciones"][0]["destino"] = "E99"
    copia = tmp_path / "copia.json"
    copia.write_text(json.dumps(datos), encoding="utf-8")
    with pytest.raises(ErrorContenido) as exc:
        cargar_historia(copia)
    assert "E99" in "\n".join(exc.value.errores)