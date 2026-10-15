# Trazabilidad – La última transmisión (v2)

**Integrante:** Cristian David Cardeño Gulloso

---

## Matriz RF → Modelo → Componente → Prueba

| ID | Descripción corta | Modelo | Componente / Archivo | Prueba / Evidencia |
|---|---|---|---|---|
| RF01 | Carga historia desde archivo JSON | CU1, Clases: `Historia`, `Escena`, `Opcion` | `motor/cargador.py::cargar_historia` | `test_integracion.py::test_i1_archivo_real_hasta_un_final` |
| RF02 | Inicia en escena `inicio` con variables iniciales | Clases: `Sesion.__init__`, `Historia` | `motor/sesion.py::Sesion.reiniciar` | `test_sesion.py::test_u5_reiniciar_restaura_estado_inicial` |
| RF03 | Distintas historias sin modificar el motor | Contexto (capa datos separada) | `historias/segunda_historia.json` + motor sin cambios | `test_segunda_historia.py` (4 pruebas); `docs/evidencia_rnf01.txt` |
| RF04 | Muestra texto de escena actual | CU2, Secuencia: mostrar escena | `cli.py::jugar` (línea `print(escena.texto)`) | Demostración manual; `test_i1_archivo_real_hasta_un_final` verifica llegada a escenas |
| RF05 | Solo opciones con condiciones cumplidas | CU2, CU3, Clases: `Sesion._habilitada` | `motor/sesion.py::opciones_disponibles` | `test_sesion.py::test_u1_condiciones_habilitan_solo_las_correspondientes` |
| RF06 | Elegir aplica efectos y avanza al destino | CU3, Secuencia: `elegir` | `motor/sesion.py::Sesion.elegir` | `test_sesion.py::test_u2_eleccion_valida_aplica_efectos_y_avanza` |
| RF07 | Opción inválida no altera estado | Secuencia: rama de error | `motor/sesion.py::Sesion.elegir` + `motor/errores.py::ErrorJugada` | `test_sesion.py::test_u3_opcion_invalida_deja_estado_intacto` |
| RF08 | Entrada de consola inválida no cierra el programa | CU3 (extensión de error) | `cli.py::jugar` (bloque `try/except` + `isdigit`) | `test_rnf.py::test_rnf03_mas_de_100_entradas_invalidas_no_producen_excepciones_no_controladas` |
| RF09 | Variables persisten durante la partida | Clases: `Sesion._variables` | `motor/sesion.py` (atributo `_variables`) | `test_integracion.py::test_i1_archivo_real_hasta_un_final` (CA01) |
| RF10 | Escena final reconocida y comunicada | CU6, Estados: `Finalizada` | `motor/sesion.py::esta_finalizada`; `cli.py` (imprime "FIN") | `test_sesion.py::test_final_se_reconoce` |
| RF11 | Reiniciar restaura estado inicial | CU5, Estados: transición `reiniciar` | `motor/sesion.py::Sesion.reiniciar` | `test_sesion.py::test_u5_reiniciar_restaura_estado_inicial` |
| RF12 | Validación completa al cargar (10 variantes) | CU7, Clases: `ErrorContenido` | `motor/cargador.py::validar_datos` | `test_validacion.py::test_u4_errores_de_contenido_son_rechazados_con_mensaje` (10 casos parametrizados) |
| RF13 | Mensajes de error con causa e ID | CU7, Clases: `ErrorContenido.errores` | `motor/cargador.py` (mensajes con contexto) | `test_validacion.py` (aserciones sobre fragmento del mensaje) |
| RF14 | Bloqueo detectado; permite reiniciar | Estados: `Bloqueada` | `motor/sesion.py::esta_bloqueada`; `cli.py` (imprime "BLOQUEO") | `test_sesion.py::test_bloqueo_en_escena_no_final_sin_opciones_habilitadas` |
| RF15 | Deshacer última elección válida | CU4, Estados: `deshacer`, Clases: `Sesion._previo` | `motor/sesion.py::Sesion.deshacer` | `test_deshacer.py::test_u6_deshacer_restaura_escena_y_variables_y_consume_retroceso` |
| RF16 | Retroceso de un solo nivel | Estados: `deshacer` (consume `_previo`) | `motor/sesion.py::Sesion.deshacer` (asigna `_previo = None`) | `test_deshacer.py::test_u6_deshacer_solo_revierte_la_ultima_eleccion` |
| RF17 | Sin retroceso al iniciar; reiniciar elimina historial | Estados: transición inicial y `reiniciar` | `motor/sesion.py::reiniciar` (asigna `_previo = None`) | `test_deshacer.py::test_u6_no_hay_retroceso_al_iniciar`; `test_u5_reiniciar_elimina_el_historial` |
| RF18 | Opción inválida no sustituye el historial previo | Secuencia: rama de error (valida antes de guardar) | `motor/sesion.py::elegir` (guarda `_previo` solo tras validar) | `test_deshacer.py::test_u6_entrada_invalida_preserva_el_historial` |
| RF19 | Deshacer desde un final | Estados: `Finalizada → EnCurso` | `motor/sesion.py::deshacer` (no distingue si es final) | `test_deshacer.py::test_u6_deshacer_desde_un_final`; `test_i1_deshacer_desde_un_final_con_archivo_real` |

---

## Matriz RNF → Procedimiento → Componente → Evidencia

| ID | Atributo | Procedimiento | Componente / Archivo | Evidencia |
|---|---|---|---|---|
| RNF01 | Modificabilidad | `git diff --stat v1-base HEAD -- motor/ cli.py` muestra 0 líneas de `motor/` cambiadas al agregar `segunda_historia.json` | `historias/segunda_historia.json`; motor sin cambios entre v1-base y adición de segunda historia | `docs/evidencia_rnf01.txt`; `tests/test_segunda_historia.py` (4 pruebas PASSED) |
| RNF02 | Claridad de errores | Prueba parametrizada con 10 variantes; cada caso afirma que el mensaje contiene causa + ID | `motor/cargador.py::validar_datos` | `tests/test_validacion.py::test_u4_errores_de_contenido_son_rechazados_con_mensaje` (10/10 PASSED) |
| RNF03 | Confiabilidad | Semilla fija SEMILLA=2026; 100+ IDs aleatorios inválidos + 10 archivos corruptos; se verifica que solo se lanzan `ErrorJugada` / `ErrorContenido` | `motor/sesion.py::elegir`; `motor/cargador.py::cargar_historia` | `tests/test_rnf.py` (11 pruebas PASSED); `docs/resultados_pruebas_v3.txt` |

---

## Cobertura de escenarios de prueba requeridos

| Escenario | Prueba(s) que lo cubre | Estado |
|---|---|---|
| U1 – Condiciones habilitan solo las correspondientes | `test_sesion.py::test_u1_condiciones_habilitan_solo_las_correspondientes` | ✅ PASSED |
| U2 – Elección válida aplica efectos y avanza | `test_sesion.py::test_u2_eleccion_valida_aplica_efectos_y_avanza` | ✅ PASSED |
| U3 – Opción inválida deja estado intacto | `test_sesion.py::test_u3_opcion_invalida_deja_estado_intacto[abrir]`; `[no_existe]` | ✅ PASSED |
| U4 – Errores de contenido producen rechazo (10 variantes) | `test_validacion.py::test_u4_errores_de_contenido_son_rechazados_con_mensaje` (10 parámetros) + 3 adicionales | ✅ PASSED |
| U5 – Reiniciar restaura estado inicial | `test_sesion.py::test_u5_reiniciar_restaura_estado_inicial`; `test_deshacer.py::test_u5_reiniciar_elimina_el_historial` | ✅ PASSED |
| U6 – Deshacer (nuevo, cambio hora 6) | `test_deshacer.py` — 8 pruebas de U6 | ✅ PASSED |
| I1 – Carga y decisiones hasta un final con archivo real | `test_integracion.py::test_i1_archivo_real_hasta_un_final`; `test_deshacer.py::test_i1_deshacer_desde_un_final_con_archivo_real`; `test_i1_ejemplo_del_anexo_de_la_hora_6` | ✅ PASSED |

---

## Cobertura de variantes de error de contenido (RF12)

| Variante | Función mutadora | Fragmento verificado | Prueba |
|---|---|---|---|
| Inicio inexistente | `_inicio` | `'X9' no existe` | `test_u4_errores_de_contenido_son_rechazados_con_mensaje[_inicio-...]` |
| ID de escena duplicado | `_escena_dup` | `ID de escena duplicado: 'A'` | `[_escena_dup-...]` |
| ID de opción duplicado | `_opcion_dup` | `ID de opción duplicado 'tomar'` | `[_opcion_dup-...]` |
| Destino inexistente | `_destino` | `'E99' no existe` | `[_destino-...]` |
| Variable no declarada (condición) | `_var_condicion` | `'fantasma' no está declarada` | `[_var_condicion-...]` |
| Variable no declarada (efecto) | `_var_efecto` | `'fantasma' no está declarada` | `[_var_efecto-...]` |
| Valor no booleano | `_no_booleano` | `no es booleano` | `[_no_booleano-...]` |
| Campo obligatorio ausente | `_falta_campo` | `falta el campo obligatorio 'titulo'` | `[_falta_campo-...]` |
| Escena final con opciones | `_final_con_opciones` | `Escena 'C': es final` | `[_final_con_opciones-...]` |
| Escena no final sin opciones | `_nofinal_sin_opciones` | `Escena 'B': no es final` | `[_nofinal_sin_opciones-...]` |
| Archivo inexistente | — | `no se encontró` | `test_u4_archivo_inexistente` |
| Archivo ilegible (JSON inválido) | — | `no es un JSON legible` | `test_u4_archivo_ilegible` |
| Estructura raíz incorrecta (lista) | — | `ErrorContenido` | `test_u4_estructura_incorrecta` |
