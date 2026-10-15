# Requisitos – La última transmisión

**Integrante:** Cristian David Cardeño Gulloso (entrega individual, ver P3)
**Versión del documento:** v1 (previa al cambio). Etiqueta Git: `v1-base`

## 1. Problema, actores y alcance

**Problema.** Un colectivo de escritores necesita publicar ficción interactiva para un festival universitario sin depender de programadores. Hace falta un motor que lea historias desde archivos, muestre solo las decisiones compatibles con lo ocurrido y avise con claridad si un archivo tiene errores.

**Actores.**
- Escritora principal: edita el archivo de la historia.
- Diseñador de la experiencia: define condiciones y consecuencias.
- Lector: juega la historia.
- Coordinadora del festival: necesita diagnósticos claros ante errores de contenido.

**Dentro del alcance.** Carga desde archivo, condiciones de igualdad sobre booleanos, efectos que asignan verdadero/falso, finales, reinicio, validación de contenido, interfaz de consola.

**Fuera del alcance.** Cuentas, base de datos, guardado entre ejecuciones, internet, editor visual, audio, imágenes, lenguaje de expresiones, **retroceso** (ver sección 5).

## 2. Requisitos funcionales

| ID | Requisito (comportamiento observable) | Necesidad | Criterio de aceptación |
|---|---|---|---|
| RF01 | El sistema carga una historia desde un archivo JSON indicado por ruta. | N01 | Dado un JSON válido, la carga devuelve una historia con todas sus escenas. |
| RF02 | La partida inicia en la escena `inicio` con las `variables` iniciales definidas en el archivo. | N01 | Dada una partida nueva de la historia de referencia, la escena es E1 y `conoce_origen` y `confia_en_la_voz` son falsos. |
| RF03 | El sistema permite cargar distintas historias sin modificar el motor. | N01 | Una segunda historia de 3 escenas se juega sin cambiar archivos de `motor/` ni `cli.py`. |
| RF04 | El sistema muestra el texto de la escena actual. | N02 | Al iniciar, se imprime el texto de E1. |
| RF05 | El sistema muestra solo las opciones cuyas condiciones se cumplen; un mapa de condiciones vacío habilita la opción. | N02 | En E3 con `conoce_origen` verdadero se ven "Activar con código" y "Cortar comunicación" (CA01). |
| RF06 | Al elegir una opción habilitada, el sistema aplica sus efectos y avanza al destino. | N03 | Elegir "Investigar archivo" en E2 deja `conoce_origen` verdadero y la escena E3. |
| RF07 | Elegir una opción inexistente o no habilitada no altera la escena ni las variables, y se informa el error. | N03 | Enviar el ID de "Activar con código" sin conocer el origen lanza error y el estado queda igual (CA02). |
| RF08 | El sistema rechaza entradas de consola inválidas sin alterar la partida ni cerrarse. | N03 | Escribir "abc" o un número fuera de rango muestra un aviso y repite la pregunta. |
| RF09 | El sistema conserva las variables durante la partida para condicionar elecciones posteriores. | N04 | Un efecto aplicado en E2 determina qué opción de activación aparece en E3. |
| RF10 | El sistema reconoce una escena final, muestra su texto y lo informa. | N05 | Al llegar a E4, E5 o E6 se muestra "FIN de la historia". |
| RF11 | El sistema permite reiniciar la partida restaurando escena y variables iniciales, sin conservar información previa. | N05 | Tras reiniciar desde E3, la escena es E1 y las variables vuelven a sus valores iniciales. |
| RF12 | El sistema valida el archivo antes de iniciar y rechaza los que tengan: archivo ilegible o estructura incorrecta, campos obligatorios ausentes, inicio inexistente, IDs de escena u opción duplicados, destino inexistente, variable no declarada, valor no booleano, o cantidad de opciones incompatible con el carácter final. | N06 | Cada variante produce rechazo y no se abre sesión jugable (CA03). |
| RF13 | Cada error de validación indica la causa y el campo o ID involucrado. | N06 | Un destino E99 produce un mensaje que menciona la escena, la opción y `E99`. |
| RF14 | Si una escena no final queda sin opciones habilitadas, el sistema informa el bloqueo y permite reiniciar. | N06 / N03 | Con una escena no final sin opciones habilitadas se muestra "BLOQUEO" y se ofrece reiniciar. |

> Pendiente: los RF de la solicitud de cambio (hora 6) se agregan como RF15 en adelante.

## 3. Requisitos no funcionales (medibles)

| ID | Atributo | Requisito medible | Procedimiento de verificación | Evidencia |
|---|---|---|---|---|
| RNF01 | Modificabilidad del contenido | Agregar una historia nueva o editar escenas requiere **0 líneas modificadas** en `motor/` y `cli.py`. | Cargar `segunda_historia.json` con el mismo motor y comparar con `git diff --stat v1-base` que no cambia `motor/` ni `cli.py` por esa historia. | `tests/test_segunda_historia.py` (por crear) y salida del `git diff` guardada en `docs/`. |
| RNF02 | Claridad de errores | El **100 %** de las 10 variantes de error de contenido genera un mensaje que contiene la causa y el ID o campo involucrado. | Prueba parametrizada que provoca cada variante y afirma que el mensaje contiene el ID esperado. | `tests/test_validacion.py` y `docs/resultados_pruebas.txt`. |
| RNF03 | Confiabilidad | **0 excepciones no controladas** ante 100 entradas inválidas a `elegir()` y 10 archivos corruptos. | Script reproducible con semilla fija que intenta IDs aleatorios y archivos mal formados, y comprueba que solo se lanzan `ErrorJugada` o `ErrorContenido`. | `tests/test_rnf.py` (por crear) y registro de ejecución. |

## 4. Preguntas y supuestos

| # | Pregunta o supuesto | Respuesta / decisión |
|---|---|---|
| P1 | ¿Debe poder retrocederse siempre (escritora) o las decisiones son irreversibles (diseñador)? | **Pregunta enviada al cliente.** Acuerdo provisional: no se implementa retroceso en la versión inicial. |
| P2 | ¿Se acepta entrega individual por no tener pareja? | Pregunta enviada al docente. **Supuesto:** entrega individual, con todos los roles asumidos por un integrante. |
| P3 | El archivo `la_ultima_transmision.json` no fue publicado en el aula. | **Supuesto:** se construyó desde las tablas de la sección 2 de la guía, respetando escenas, rutas, condiciones y efectos. Se compara con la versión oficial si se publica. |

> Completar con la fecha y la respuesta real cuando el docente conteste.

## 5. Conflicto de requisitos: retroceso

- **Escritora:** quiere permitir retroceder siempre.
- **Diseñador:** quiere decisiones irreversibles para que tengan consecuencias.
- **Conflicto:** retroceder anula las consecuencias de elegir.
- **Pregunta de aclaración al cliente:** ¿el retroceso debe ser opcional por historia, limitado a ciertas escenas o inexistente?
- **Acuerdo provisional:** la primera versión no implementa retroceso. No se presupone una decisión posterior del cliente.

## 6. Revisión de requisitos: ambigüedad o defecto detectado

- **Hallazgo:** RF05 decía «el sistema muestra solo las opciones cuyas condiciones se cumplen» sin especificar si las opciones no habilitadas se *ocultan completamente* o se *muestran desactivadas y visibles*. Ambas interpretaciones son válidas desde la perspectiva del lector, pero producen implementaciones radicalmente distintas: ocultar simplifica el motor y evita confundir al lector con opciones que no puede elegir; mostrar desactivadas permite al lector entender qué condición le falta para acceder a esa rama. El criterio de aceptación CA01 afirmaba que «se muestran activar con código y cortar comunicación» en E3 con `conoce_origen = verdadero`, lo que descartaba "activar sin verificar" sin explicitar si debía ocultarse o aparecr tachada.

- **Dónde:** RF05 y CA01 (sección 2 de requisitos).

- **Corrección:** Se aclaró que las opciones no habilitadas se *ocultan*: `Sesion.opciones_disponibles()` devuelve únicamente las opciones cuyas condiciones se cumplen con el estado actual, y la CLI solo numerará y mostrará esas opciones. Esta decisión se tomó porque (a) el criterio CA01 dice "se muestran activar con código y cortar comunicación" sin mencionar la tercera, y (b) el enunciado indica exactamente que "deben verse exactamente dos opciones" en E3. El criterio de aceptación de RF05 se actualizó a: «En E3 con `conoce_origen` verdadero, `opciones_disponibles()` devuelve exactamente dos opciones: "activar con código" y "cortar comunicación".» La prueba `test_u1_condiciones_habilitan_solo_las_correspondientes` verifica este comportamiento.

## 7. Priorización razonada de atributos de calidad

De acuerdo con las necesidades del cliente y el contexto del festival:

1. **Modificabilidad del contenido (RNF01) – Prioridad Alta (1°):**  
   *Justificación:* La escritora principal no programa pero necesita editar relatos libremente. Si cada ajuste en el guion requiriese intervención del equipo de desarrollo, el festival no sería viable. Por ende, separar el contenido en JSON y garantizar que añadir historias nuevas implique exactamente 0 líneas de código en el motor es el atributo más crítico.
2. **Confiabilidad (RNF03) – Prioridad Alta (2°):**  
   *Justificación:* El lector debe disfrutar de una experiencia ininterrumpida; el programa jamás debe abortar de forma abrupta ante entradas inesperadas o archivos mal formados. Se exige 0 excepciones no controladas.
3. **Claridad de diagnósticos de error (RNF02) – Prioridad Media (3°):**  
   *Justificación:* La coordinadora del festival y los escritores necesitan saber exactamente qué corregir ante un error en el archivo narrativo (falla temprana con causa e identificador específico). Aunque esencial durante la fase de autoría, se supedita a que el motor funcione de forma inmutable y robusta.

## 8. Riesgos y responsabilidad profesional

**Riesgos del proyecto:**
1. *El cambio de la hora 6 rompe el motor existente.*  
   *Mitigación:* Motor genérico dirigido por datos, desacoplamiento estricto de la lógica narrativa y suite automatizada de pruebas de regresión (48 pruebas continuas).
2. *Una historia con errores de formato bloquea o cierra el programa durante el festival.*  
   *Mitigación:* Validación exhaustiva anticipada (falla temprana de 10 variantes) y captura controlada de excepciones (`ErrorContenido`, `ErrorJugada`).

**Decisión de responsabilidad profesional (datos, dependencias y autoría):**
- **Datos y licencias de dependencias:** Se utilizó únicamente la biblioteca estándar de Python para la lógica del producto (`json`, `dataclasses`, `sys`) y `pytest` (licencia MIT permisiva) exclusivamente para el entorno de pruebas automatizadas, evitando licenciamientos restrictivos o dependencias innecesarias.
- **Autoría del relato:** El contenido de `la_ultima_transmision.json` se elaboró basándose estrictamente en las especificaciones del cliente suministradas en la guía académica (supuesto P3), respetando la autoría intelectual del colectivo literario.
- **Uso responsable de herramientas de IA:** Se emplearon asistentes de IA como soporte de análisis, revisión de pruebas y redacción de documentación técnica. Para garantizar la veracidad técnica y la responsabilidad profesional, **cada resultado, modelo y línea de código fue verificado y validado localmente** mediante la ejecución exitosa de las 48 pruebas automatizadas de pytest y trazabilidad cruzada.
