# Documentación Técnica y Académica — La última transmisión

En esta carpeta se encuentran todos los documentos y evidencias exigidos por la guía del parcial práctico de Ingeniería de Software (P202602), organizados por área temática.

---

## 📑 Informes y Entrega Oficial

| Documento | Descripción |
|---|---|
| [**`informe.md`**](informe.md) | **Informe Académico Principal** (máx. 8 páginas de cuerpo). Integra las competencias de las 7 unidades: fundamentos, procesos, agilidad, requerimientos, modelado, arquitectura e implementación/cambio. |
| [**`anexo.md`**](anexo.md) | **Anexo Técnico Oficial**. Contiene todos los diagramas del sistema, capturas de tableros Kanban, matriz de trazabilidad y el guion paso a paso para el video de 6 minutos. |

---

## 🏛️ Especificación y Diseño del Sistema

| Documento | Descripción |
|---|---|
| [**`requisitos.md`**](requisitos.md) | Especificación de los 19 requisitos funcionales (RF01–RF19), 3 no funcionales (RNF01–RNF03), preguntas/supuestos, priorización de calidad y revisión de ambigüedades. |
| [**`modelos.md`**](modelos.md) | Los 5 modelos del dominio: Diagrama de Contexto, Diagrama de Casos de Uso, Diagrama de Clases, Diagrama de Secuencia (`elegir`) y Diagrama de Estados de Sesión. |
| [**`arquitectura.md`**](arquitectura.md) | Diagrama de componentes en 3 capas desacopladas, responsabilidades y documentación de decisiones D1 (conducido por datos) y D2 (falla temprana). |

---

## 🔄 Proceso y Gestión del Cambio

| Documento | Descripción |
|---|---|
| [**`proceso.md`**](proceso.md) | Justificación del proceso Incremental + Kanban vs. Cascada, prácticas ágiles aplicadas (WIP=2, pruebas continuas), DoD y mejora continua. |
| [**`cambio.md`**](cambio.md) | Gestión de la solicitud de cambio de la hora 6 (función deshacer de un solo nivel), análisis de impacto y diseño de instantánea única. |
| [**`trazabilidad.md`**](trazabilidad.md) | Matriz completa de trazabilidad cruzada que vincula cada RF y RNF con sus modelos, componentes de código y pruebas automatizadas. |

---

## 📊 Evidencias de Verificación y Pruebas

| Archivo | Contenido |
|---|---|
| [**`evidencia_rnf01.txt`**](evidencia_rnf01.txt) | Salida del comando `git diff` que demuestra **0 líneas modificadas** en el motor para soportar la segunda historia. |
| [**`resultados_pruebas_v3.txt`**](resultados_pruebas_v3.txt) | Registro de la última ejecución de pytest: **48 pruebas PASSED en 0.39 s**. |
| [**`historial_git.txt`**](historial_git.txt) | Historial exportado de Git con autores, fechas, mensajes y etiquetas (`v1-base`, `v1-pre-cambio`, `v2-deshacer`). |
| [**`tablero_inicial.png`**](tablero_inicial.png) | Captura del tablero Kanban en el estado inicial (Hora 0 / `v1-base`). |
| [**`tablero_final.png`**](tablero_final.png) | Captura del tablero Kanban en el estado de cierre (Hora 12 / `v2-deshacer`). |
