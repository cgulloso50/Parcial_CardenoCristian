import json

from motor.errores import ErrorContenido
from motor.modelos import Escena, Historia, Opcion

CAMPOS_HISTORIA = {"titulo": str, "inicio": str, "variables": dict, "escenas": list}
CAMPOS_ESCENA = {"id": str, "texto": str, "final": bool, "opciones": list}
CAMPOS_OPCION = {"id": str, "texto": str, "destino": str,
                 "condiciones": dict, "efectos": dict}


def _faltantes(obj, campos, contexto):
    """Devuelve errores de campos ausentes o con tipo incorrecto."""
    errores = []
    for campo, tipo in campos.items():
        if campo not in obj:
            errores.append(f"{contexto}: falta el campo obligatorio '{campo}'")
        elif not isinstance(obj[campo], tipo):
            errores.append(f"{contexto}: el campo '{campo}' tiene un tipo incorrecto")
    return errores


def validar_datos(datos):
    """Devuelve la lista de errores de contenido (vacía si es válido)."""
    if not isinstance(datos, dict):
        return ["Historia: la estructura raíz debe ser un objeto JSON"]
    errores = _faltantes(datos, CAMPOS_HISTORIA, "Historia")
    if errores:
        return errores

    variables = datos["variables"]
    for nombre, valor in variables.items():
        if not isinstance(valor, bool):
            errores.append(f"Variable '{nombre}': el valor inicial no es booleano")

    ids_escenas = set()
    escenas_validas = []
    for i, esc in enumerate(datos["escenas"]):
        if not isinstance(esc, dict):
            errores.append(f"Escena en posición {i}: debe ser un objeto")
            continue
        errores += _faltantes(esc, CAMPOS_ESCENA, f"Escena en posición {i}")
        if not isinstance(esc.get("id"), str):
            continue
        if esc["id"] in ids_escenas:
            errores.append(f"ID de escena duplicado: '{esc['id']}'")
        ids_escenas.add(esc["id"])
        if isinstance(esc.get("opciones"), list) and isinstance(esc.get("final"), bool):
            escenas_validas.append(esc)

    if datos["inicio"] not in ids_escenas:
        errores.append(f"Inicio: la escena '{datos['inicio']}' no existe")

    for esc in escenas_validas:
        eid = esc["id"]
        if esc["final"] and esc["opciones"]:
            errores.append(f"Escena '{eid}': es final y debe tener 0 opciones")
        if not esc["final"] and not esc["opciones"]:
            errores.append(f"Escena '{eid}': no es final y debe tener al menos una opción")
        ids_opciones = set()
        for j, op in enumerate(esc["opciones"]):
            if not isinstance(op, dict):
                errores.append(f"Escena '{eid}', opción en posición {j}: debe ser un objeto")
                continue
            ctx = f"Escena '{eid}', opción '{op.get('id', j)}'"
            errores += _faltantes(op, CAMPOS_OPCION, ctx)
            if isinstance(op.get("id"), str):
                if op["id"] in ids_opciones:
                    errores.append(f"Escena '{eid}': ID de opción duplicado '{op['id']}'")
                ids_opciones.add(op["id"])
            if isinstance(op.get("destino"), str) and op["destino"] not in ids_escenas:
                errores.append(f"{ctx}: el destino '{op['destino']}' no existe")
            for clave in ("condiciones", "efectos"):
                mapa = op.get(clave)
                if not isinstance(mapa, dict):
                    continue
                for var, valor in mapa.items():
                    if var not in variables:
                        errores.append(f"{ctx}: la variable '{var}' no está declarada en {clave}")
                    elif not isinstance(valor, bool):
                        errores.append(f"{ctx}: el valor de '{var}' en {clave} no es booleano")
    return errores


def construir_historia(datos):
    """Valida y construye la Historia. Lanza ErrorContenido si hay errores."""
    errores = validar_datos(datos)
    if errores:
        raise ErrorContenido(errores)
    escenas = {}
    for e in datos["escenas"]:
        opciones = tuple(
            Opcion(o["id"], o["texto"], o["destino"], dict(o["condiciones"]), dict(o["efectos"]))
            for o in e["opciones"]
        )
        escenas[e["id"]] = Escena(e["id"], e["texto"], e["final"], opciones)
    return Historia(datos["titulo"], datos["inicio"], dict(datos["variables"]), escenas)


def cargar_historia(ruta):
    """Lee un archivo JSON y devuelve la Historia, o lanza ErrorContenido."""
    try:
        with open(ruta, encoding="utf-8") as f:
            datos = json.load(f)
    except FileNotFoundError:
        raise ErrorContenido([f"Archivo: no se encontró '{ruta}'"])
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        raise ErrorContenido([f"Archivo: '{ruta}' no es un JSON legible ({e})"])
    return construir_historia(datos)
