# Documentación Técnica — La última transmisión

En esta carpeta se encuentran los documentos técnicos de diseño, arquitectura, requisitos y verificación del motor interactivo.

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
| [**`tablero_inicial.png`**](tablero_inicial.png) | Captura del tablero Kanban inicial (reconstruido en Microsoft Planner a partir del backlog). |
| [**`tablero_final.png`**](tablero_final.png) | Captura del tablero Kanban final con la totalidad de tareas completadas. |

---

## 📄 Informes y Anexos Técnicos

| Documento | Formato Markdown | Formato HTML | Descripción |
|---|---|---|---|
| **Informe Final** | [**`informe.md`**](informe.md) | [**`informe.html`**](informe.html) | Informe técnico principal según la estructura de la guía (Unidades 1 a 7). |
| **Anexo Técnico** | [**`anexo.md`**](anexo.md) | [**`anexo.html`**](anexo.html) | Anexo técnico con capturas de tableros, diagramas Mermaid, matriz de trazabilidad y guion de video. |
| **Historial Git** | [**`historial_git.txt`**](historial_git.txt) | Texto plano | Log completo de commits y etiquetas del repositorio. |
