import sys

from motor.cargador import cargar_historia
from motor.errores import ErrorContenido, ErrorJugada
from motor.sesion import Sesion

RUTA_POR_DEFECTO = "historias/la_ultima_transmision.json"


def jugar(sesion):
    while True:
        print(f"\n--- {sesion.escena_actual.id} ---\n{sesion.escena_actual.texto}")
        opciones = sesion.opciones_disponibles()
        if sesion.esta_finalizada():
            print("\nFIN de la historia.")
        elif sesion.esta_bloqueada():
            print("\nBLOQUEO: no hay opciones disponibles en esta escena.")
        else:
            for n, o in enumerate(opciones, 1):
                print(f"  {n}. {o.texto}")

        comandos = "r = reiniciar, "
        if sesion.puede_deshacer():
            comandos += "d = deshacer, "
        comandos += "q = salir"
        entrada = input(f"Elija una opción ({comandos}): ").strip().lower()

        if entrada == "q":
            return
        if entrada == "r":
            sesion.reiniciar()
            print("\n>>> Partida reiniciada.")
            continue
        if entrada == "d":
            try:
                sesion.deshacer()
                print("\n>>> Última decisión deshecha.")
            except ErrorJugada as e:
                print(f"Error: {e}")
            continue
        if not entrada.isdigit() or not 1 <= int(entrada) <= len(opciones):
            print("Entrada no válida.")
            continue
        try:
            sesion.elegir(opciones[int(entrada) - 1].id)
        except ErrorJugada as e:
            print(f"Error: {e}")


def main():
    ruta = sys.argv[1] if len(sys.argv) > 1 else RUTA_POR_DEFECTO
    try:
        historia = cargar_historia(ruta)
    except ErrorContenido as e:
        print("No se puede iniciar. La historia tiene errores:")
        for linea in e.errores:
            print(f"  - {linea}")
        return 1
    print(f"=== {historia.titulo} ===")
    jugar(Sesion(historia))
    return 0


if __name__ == "__main__":
    sys.exit(main())
    