import sys

from motor.cargador import cargar_historia
from motor.errores import ErrorContenido, ErrorJugada
from motor.sesion import Sesion

RUTA_POR_DEFECTO = "historias/la_ultima_transmision.json"


def jugar(sesion):
    while True:
        print(f"\n--- {sesion.escena_actual.id} ---\n{sesion.escena_actual.texto}")
        if sesion.esta_finalizada():
            print("\nFIN de la historia.")
            if input("¿Jugar de nuevo? (s/n): ").strip().lower() == "s":
                sesion.reiniciar()
                continue
            return
        if sesion.esta_bloqueada():
            print("\nBLOQUEO: no hay opciones disponibles en esta escena.")
            if input("¿Reiniciar? (s/n): ").strip().lower() == "s":
                sesion.reiniciar()
                continue
            return
        opciones = sesion.opciones_disponibles()
        for n, o in enumerate(opciones, 1):
            print(f"  {n}. {o.texto}")
        entrada = input("Elija una opción (r = reiniciar, q = salir): ").strip().lower()
        if entrada == "q":
            return
        if entrada == "r":
            sesion.reiniciar()
            continue
        if not entrada.isdigit() or not 1 <= int(entrada) <= len(opciones):
            print("Entrada no válida. Escriba el número de una opción.")
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
