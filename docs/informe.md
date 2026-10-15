# Informe Final – Parcial Práctico de Ingeniería de Software
## Proyecto: *La última transmisión* (Motor de Ficción Interactiva)

**Estudiante:** Cristian David Cardeño Gulloso  
**Modalidad:** Entrega individual (supuesto P2 documentado)  
**Asignatura:** Ingeniería de Software  
**Fecha:** Octubre 2026  

---

## 1. Fundamentos del Problema y Alcance (Unidad 1)

### 1.1. Contexto y Problema
Un colectivo de escritores independientes prepara una experiencia de ficción interactiva para un festival universitario. En la obra de referencia, una operadora de radio recibe una señal desde la estación polar Aurora, abandonada hace dos décadas. Cada lector debe poder tomar decisiones que bifurquen la narrativa hacia múltiples desenlaces según las pistas descubiertas.  
El problema central radica en que los autores literarios no poseen conocimientos de programación, pero requieren diseñar, iterar y distribuir relatos interactivos sin requerir intervenciones continuas del equipo técnico de software. Asimismo, los lectores requieren una experiencia inmersiva libre de fallos abruptos, y la coordinación del festival requiere diagnósticos transparentes y tempranos si un archivo presenta inconsistencias.

### 1.2. Actores Involucrados
- **Escritora principal:** Autora del contenido; crea y modifica escenas, opciones y consecuencias directamente sobre archivos de datos estructurados (JSON).
- **Diseñador narrativo:** Modela la lógica del juego, dependencias causales, condiciones habilitantes y efectos.
- **Lector / Jugador:** Interactúa con el relato a través de la interfaz de consola, tomando decisiones y descubriendo desenlaces.
- **Coordinadora del festival:** Responsable de la puesta a punto del material; necesita informes legibles de error si un archivo narrativo no cumple el contrato.

### 1.3. Alcance del Sistema
- **Dentro del alcance:** Motor determinista dirigido por datos; carga de historias en formato JSON estándar; evaluación de precondiciones booleanas de igualdad; aplicación de efectos de mutación booleana; navegación no lineal por grafos de escenas; detección de escenas finales y callejones sin salida (bloqueos); reinicio a estado original; mecanismo de retroceso de un nivel (`deshacer`); validación sintáctica y semántica exhaustiva previa a la partida; interfaz de consola desacoplada.
- **Fuera del alcance:** Persistencia en bases de datos o almacenamiento en disco de partidas guardadas; cuentas de usuario o perfiles; soporte de red/multijugador; renderizado de imágenes, sonido o video; lenguaje de expresiones aritméticas complejas.

### 1.4. Gestión de Riesgos
1. **Riesgo 1 (Impacto del cambio a mitad del ciclo):** La introducción de una solicitud de cambio a las 6 horas de desarrollo podría quebrar la arquitectura inicial y generar regresiones en el motor.  
   *Mitigación:* Se implementó un núcleo puramente conducido por datos (*data-driven*) sin lógica acoplada a escenas específicas, complementado con una suite de pruebas automatizadas continua (pytest) que alerta de cualquier ruptura en menos de 0.5 segundos.
2. **Riesgo 2 (Contenido corrupto o inconsistente en producción):** Un relato con errores estructurales podría provocar caídas inesperadas (`crashes`) durante la interacción del público.  
   *Mitigación:* Arquitectura de falla temprana que valida 10 variantes de inconsistencia antes de instanciar la sesión jugable, emitiendo diagnósticos controlados que identifican la causa exacta y el elemento afectado.

### 1.5. Priorización Razonada de Atributos de Calidad
1. **Modificabilidad del contenido (RNF01) – Prioridad Máxima:** Es la razón de ser del encargo. La adición de relatos o edición de escenas debe requerir exactamente 0 líneas de código modificadas en el motor o interfaz.
2. **Confiabilidad (RNF03) – Prioridad Alta:** Ante cualquier entrada del usuario (caracteres extraños, números fuera de rango, IDs no habilitados) o ante archivos JSON mutilados, el sistema garantiza 0 excepciones no controladas.
3. **Claridad de diagnósticos de error (RNF02) – Prioridad Media:** Todo error en el archivo de historia se comunica identificando el campo, la escena u opción involucrada.

### 1.6. Decisión de Responsabilidad Profesional
- **Dependencias y Licencias:** Se eligió intencionalmente usar únicamente la biblioteca estándar de Python para el motor y CLI (`json`, `dataclasses`, `sys`), y la biblioteca `pytest` (licencia permisiva MIT) exclusivamente para el desarrollo y automatización de pruebas.
- **Autoría:** El relato de referencia `la_ultima_transmision.json` fue transcrito y estructurado fielmente respetando el diseño del cliente. La segunda historia `segunda_historia.json` fue ideada como demostración técnica sin plagiar fuentes externas.
- **Uso de Herramientas de IA:** Se utilizaron modelos de IA para asistencia en la estructuración de pruebas de borde y redacción técnica. **Cada modelo, código y prueba fue verificado localmente**, asegurando que el 100% de las 48 pruebas automatizadas pasen en el entorno de ejecución real.

---

## 2. Proceso y Ciclo de Vida (Unidad 2)

Se seleccionó un **modelo de proceso incremental guiado por Kanban**, estructurado en dos iteraciones delimitadas:
- **Versión 1 (v1-base, Horas 0 a 6):** Cubre el alcance inicial (carga, navegación, condiciones, efectos, validación, consola y suite base U1–U5, I1).
- **Versión 2 (v2-deshacer, Horas 6 a 12):** Incorpora la solicitud de cambio (RF15–RF19: retroceso de un solo nivel), verificación de RNF y segunda historia.

### Comparación con Cascada Tradicional
| Criterio | Incremental + Kanban (Elegido) | Cascada Tradicional (Descartado) |
|---|---|---|
| Capacidad de cambio | El cambio de la hora 6 se integra sobre una base probada sin rehacer todo el sistema. | El cambio obligaría a retroceder y reabrir fases congeladas con alto retrabajo. |
| Gestión del riesgo | Pruebas ejecutadas continuamente desde la primera hora; fallas detectadas al instante. | Las pruebas se retrasan al final del ciclo, acumulando incertidumbre. |
| Evidencia tangible | Commits atómicos, tags Git y tablero que reflejan la evolución real paso a paso. | Un solo entregable monolítico al final del plazo. |

---

## 3. Prácticas Ágiles y Trabajo en Equipo (Unidad 3)

1. **Tablero Kanban con Límite de Trabajo en Curso (WIP = 2):** Permitió evitar la dispersión de esfuerzos al mantener únicamente dos tarjetas en curso simultáneamente. Evidenciado en `docs/tablero_inicial.png` y `docs/tablero_final.png`.
2. **Pruebas Automatizadas Continuas con Commits Pequeños:** Cada incremento funcional se desarrolló en conjunto con su prueba unitaria o de integración correspondiente, corriendo `pytest` antes de cada commit.
3. **Práctica Descartada (Programación en Pareja):** Debido a la modalidad individual, se sustituyó la revisión en parejas por una rigurosa autorrevisión diferida en el tiempo y validación automatizada por suites de prueba.
4. **Definición de Terminado (DoD):** Una tarjeta se consideró terminada únicamente si poseía código versionado en Git, pruebas automatizadas en verde, manejo controlado de errores, documentación actualizada y cumplimiento de trazabilidad.
5. **Aprendizaje y Mejora:** Se identificó en la primera hora que iniciar el desarrollo sin verificar la presencia física de los JSON generaba pérdidas de tiempo. Se adoptó como acción de mejora la verificación inmediata de precondiciones de entrada en cada ciclo.

---

## 4. Requerimientos del Sistema (Unidad 4)

Se formularon 19 Requisitos Funcionales propios y atómicos, cubriendo integralmente las necesidades del cliente N01 a N06:
- **N01 (Distribución y arranque):** RF01 (carga JSON), RF02 (estado inicial), RF03 (historias múltiples sin tocar motor).
- **N02 (Lectura y opciones condicionales):** RF04 (mostrar texto de escena), RF05 (filtrar opciones según condiciones).
- **N03 (Consecuencias y robustez de entrada):** RF06 (aplicación de efectos y avance), RF07 (estado intacto ante opción inválida), RF08 (rechazo de entradas inválidas de consola sin caída).
- **N04 (Persistencia de contexto):** RF09 (persistencia de variables durante la partida).
- **N05 (Desenlaces y reinicio):** RF10 (reconocimiento de escenas finales), RF11 (reinicio a estado original).
- **N06 (Diagnóstico y prevención):** RF12 (validación previa completa de 10 variantes), RF13 (diagnóstico con causa e ID), RF14 (detección de bloqueo en escenas no finales).
- **Solicitud de Cambio (Hora 6):** RF15 (deshacer última decisión válida), RF16 (límite de un nivel de retroceso), RF17 (sin retroceso inicial ni tras reiniciar), RF18 (entrada inválida no altera historial de retroceso), RF19 (retroceso habilitado desde escenas finales).

### Requisitos No Funcionales Medibles
- **RNF01 (Modificabilidad):** Agregar una historia nueva requiere **0 líneas modificadas** en `motor/` y `cli.py`. Verificado con `git diff --stat v1-base HEAD -- motor/ cli.py` y `tests/test_segunda_historia.py`.
- **RNF02 (Claridad de errores):** El **100% de las 10 variantes** de error de contenido emite un mensaje con la causa y el identificador del campo o escena involucrado. Verificado en `tests/test_validacion.py`.
- **RNF03 (Confiabilidad):** **0 excepciones no controladas** ante más de 100 elecciones aleatorias inválidas y 10 archivos corruptos. Verificado en `tests/test_rnf.py`.

### Revisión de Requisitos (Ambigüedad Detectada)
En la revisión de la especificación inicial, se detectó que **RF05** no explicitaba si las opciones no habilitadas debían *ocultarse* o mostrarse *desactivadas/visibles*. Conforme al criterio CA01 y el requerimiento de que en E3 se presenten exactamente dos opciones, se corrigió RF05 estipulando formalmente que las opciones que no cumplan sus condiciones se excluyen de la lista disponible.

---

## 5. Modelado del Dominio (Unidad 5)

*(Ver Anexo para los diagramas Mermaid completos)*
- **Diagrama de Contexto:** Delimita las interacciones entre Escritora, Diseñador, Coordinadora, Lector y el Motor interactivo.
- **Diagrama de Casos de Uso:** Modela CU1 (Cargar historia), CU2 (Ver escena), CU3 (Elegir opción), CU4 (Deshacer decisión), CU5 (Reiniciar), CU6 (Reconocer final) y CU7 (Diagnóstico).
- **Diagrama de Clases:** `Historia`, `Escena` y `Opcion` modeladas como `dataclass(frozen=True)` inmutables; `Sesion` encapsula el estado mutable (`_escena_id`, `_variables`, `_previo`); jerarquía de excepciones `ErrorMotor` → `ErrorContenido`, `ErrorJugada`.
- **Diagrama de Secuencia (Elegir Opción):** Detalla el flujo desde la entrada del lector en CLI, validación de existencia y habilitación en `Sesion`, preservación del estado previo, aplicación de efectos y transición de escena.
- **Diagrama de Estados:** Modela los estados de `Sesion` (`EnCurso`, `Finalizada`, `Bloqueada`) y sus transiciones ante `elegir`, `deshacer` y `reiniciar`.

---

## 6. Arquitectura del Software (Unidad 6)

### 6.1. Estilo Arquitectónico en Capas Unidireccionales
El sistema adopta una arquitectura desacoplada en tres capas estrictas:
1. **Capa de Contenido (Datos):** Archivos JSON declarativos puros (`historias/*.json`).
2. **Capa de Reglas de Negocio (`motor/`):** Modelos de datos inmutables, cargador/validador y máquina de estado de la partida (`sesion.py`).
3. **Capa de Interfaz (`cli.py`):** Presentación por terminal y captura de comandos de usuario.

### 6.2. Decisiones Arquitectónicas Fundamentales
- **Decisión D1 (Historias conducidas por datos JSON vs. codificadas en el programa):**  
  *Elección:* Almacenar escenas y lógica en JSON interpretado por un motor genérico.  
  *Consecuencias:* Permite cumplir RNF01 (0 líneas de código modificadas para nuevos relatos). Exige incorporar un validador sintáctico/semántico riguroso.
- **Decisión D2 (Validación por falla temprana exhaustiva vs. validación perezosa durante la partida):**  
  *Elección:* Analizar la totalidad del archivo antes de iniciar y abortar si existe algún error.  
  *Consecuencias:* Cumple RNF02; el autor recibe todos los problemas detectados en un solo informe; la sesión en curso opera bajo la garantía de integridad referencial absoluta.

---

## 7. Implementación, Gestión del Cambio y Pruebas (Unidad 7)

### 7.1. Decisión de Diseño Detallado: Desacoplamiento e Inmutabilidad
- Las clases `Historia`, `Escena` y `Opcion` son inmutables (`frozen=True`). `Sesion` no puede corromper el contenido cargado.
- La propiedad `Sesion.variables` retorna una copia del diccionario interno, asegurando que agentes externos no puedan alterar el estado sin invocar `elegir()`, `deshacer()` o `reiniciar()`.
- La instantánea de retroceso `_previo` solo se genera después de validar que la jugada es legal, asegurando que jugadas erróneas no destruyan el historial previo (RF18).

### 7.2. Incorporación de la Solicitud de Cambio (Hora 6)
Al recibir la solicitud de incorporar la función de retroceso de un solo nivel, se realizó el análisis de impacto (`docs/cambio.md`):
- Se extendió `motor/sesion.py` incorporando el atributo `_previo = (escena_id, dict(variables))` y los métodos `puede_deshacer()` y `deshacer()`.
- Se adaptó `cli.py` para exponer dinámicamente el comando `d` cuando exista retroceso disponible.
- Los componentes `cargador.py`, `modelos.py` y los archivos JSON no requirieron modificación alguna.

### 7.3. Cobertura y Resultados de Pruebas Automatizadas
La suite final consta de **48 pruebas automatizadas** que se ejecutan en **0.39 segundos** con resultado **100% PASSED**:
- **Unitarias (U1 a U5):** Condiciones habilitantes, efectos, aislamiento ante errores, reinicio, finales y bloqueos (`test_sesion.py`).
- **Validación (U4):** 10 variantes de contenido más archivos corruptos e inexistentes (`test_validacion.py`).
- **Cambio (U6 y extensiones):** Comportamiento de retroceso en partidas normales y desde finales (`test_deshacer.py`).
- **Integración (I1 y CA01–CA03):** Recorrido completo con archivo real (`test_integracion.py`).
- **Requisitos No Funcionales:** Verificación de RNF01 (`test_segunda_historia.py`) y RNF03 (`test_rnf.py`).

---

## 8. Conclusiones
El proyecto demuestra que la aplicación rigurosa de principios de ingeniería de software (diseño por capas, fallas tempranas, inmutabilidad y pruebas continuas) permite construir un motor flexible y robusto. La incorporación del cambio a mitad del ciclo se realizó de manera ordenada, predecible y con cero regresiones en el sistema.
