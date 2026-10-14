# Proceso y agilidad – La última transmisión

**Integrante:** Cristian David Cardeño Gulloso (entrega individual)

## 1. Proceso elegido: incremental con tablero Kanban

Se trabaja en **incrementos pequeños y verificables** gestionados con un tablero Kanban (*Por hacer / En curso / Hecho*). Hay dos versiones planificadas: **v1** (alcance inicial, etiqueta `v1-base`) y **v2** (después de la solicitud de cambio de la hora 6).

**Por qué.** El enunciado ya anuncia un cambio a mitad de la ventana. Un proceso que acepta cambios sin rehacer todo encaja con ese requisito. Además, la entrega es de una sola persona y de 12 horas, así que no justifica ceremonias pesadas.

**Alternativa comparada: cascada.**

| Aspecto | Incremental + Kanban (elegido) | Cascada (alternativa) |
|---|---|---|
| Cambio de la hora 6 | Se incorpora sobre una versión ya probada | Obliga a reabrir requisitos, diseño y pruebas ya cerrados |
| Riesgo | Se detecta pronto: las pruebas corren desde el primer incremento | Se detecta al final, cuando queda poco tiempo |
| Evidencia | Commits y tablero muestran la evolución | Un solo bloque de entrega difícil de verificar |
| Costo | Requiere disciplina para mantener documentos al día | Menos actualizaciones, pero más retrabajo |

**Decisión.** Se descarta cascada porque el cambio anunciado rompería su secuencia, y no se usa Scrum completo porque sus roles y reuniones no aplican a una sola persona.

## 2. Cómo se realiza cada actividad en esta entrega

| Actividad | Qué se hace | Evidencia |
|---|---|---|
| Especificación | RF con criterio de aceptación, 3 RNF medibles, preguntas y supuestos | `docs/requisitos.md` |
| Desarrollo | Núcleo genérico primero (`Sesion`), luego cargador, CLI y segunda historia | `motor/`, `cli.py`, historial de Git |
| Validación | Pruebas automatizadas U1–U5, I1 y CA01–CA03, más recorrido manual de los tres finales | `tests/`, `docs/resultados_pruebas.txt` |
| Evolución | A la hora 6: etiqueta `v1-base`, análisis de impacto, implementación, pruebas, etiqueta `v2` | Etiquetas de Git, `docs/trazabilidad.md` |

## 3. Backlog y tablero

El backlog se mantiene en el tablero, con responsable (único integrante) y fecha. Se toman **dos capturas**: inicial (antes de mover tarjetas) y final (antes de entregar). Tras la hora 6 se añaden las tarjetas de la solicitud de cambio y se marcan como "afectadas" las tarjetas previas que dependen de ellas.

Archivos de evidencia: `docs/tablero_inicial.png`, `docs/tablero_final.png`.

## 4. Dos prácticas ágiles aplicadas y una descartada

**Práctica 1: tablero Kanban con límite de trabajo en curso (WIP = 2).**
Solo se mantienen dos tarjetas en "En curso" a la vez. Evita abrir muchos frentes y deja claro qué falta. *Evidencia:* capturas del tablero.

**Práctica 2: pruebas automatizadas continuas con commits pequeños.**
Cada incremento se acompaña de pruebas y se ejecuta `python -m pytest -v` antes de cada commit. Al llegar el cambio, las pruebas muestran de inmediato qué se rompió. *Evidencia:* `tests/`, historial de commits, registros de ejecución.

**Alternativa descartada: programación en pareja.**
Se descarta porque la entrega es individual y no hay segunda persona disponible. Su efecto de revisión se reemplaza por una autorrevisión de requisitos separada en el tiempo y por las pruebas automatizadas.

## 5. Definición de terminado

Una tarjeta pasa a "Hecho" solo si cumple todo lo que le aplique:

1. El código o documento está en el repositorio, con commit y mensaje descriptivo.
2. Existe al menos una prueba automatizada que cubre su comportamiento, y `python -m pytest -v` pasa completo.
3. Los errores esperados producen mensajes controlados, sin cierre inesperado.
4. Los documentos afectados (requisitos, modelos, trazabilidad) reflejan la versión actual.
5. Funciona siguiendo únicamente el README en un equipo limpio.
6. La tarjeta tiene su evidencia localizable (ruta de archivo o commit).

## 6. Aprendizaje y acción de mejora

**Aprendizaje.** Las primeras pruebas de integración fallaron porque `historias/la_ultima_transmision.json` estaba vacío. El motor respondió con un error controlado, pero se perdió tiempo por no verificar el insumo al empezar.

**Acción de mejora.** En los siguientes incrementos, verificar los archivos de entrada (existencia y contenido) como primer paso, y ejecutar las pruebas de integración justo después de cualquier cambio en `historias/`.

> Si encuentra un aprendizaje distinto durante el trabajo (por ejemplo, después de la hora 6), puede reemplazar o sumar uno más. Debe ser algo que realmente ocurrió.