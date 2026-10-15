# La última transmisión — Motor de ficción interactiva

**Integrante:** Cristian David Cardeño Gulloso  
**Parcial práctico de Ingeniería de Software**  
**Repositorio:** https://github.com/cgulloso50/la_ultima_transmision.json  
**Video de sustentación (Google Drive):** https://drive.google.com/file/d/1lawAyWL4AtqU6TxzOjwR42kpyM4F0g-7/view?usp=sharing

---

## Enlace del video de sustentación
- **URL Google Drive:** https://drive.google.com/drive/folders/sustentacion-parcial-cardeno

---

## Requisitos

- Python 3.12 o superior (probado con Python 3.12.9 y 3.14.7)
- No se requieren dependencias externas para ejecutar el motor ni la CLI
- Para ejecutar las pruebas: `pytest` (se instala desde `requirements.txt`)

---

## Instalación

```bash
# 1. Clonar o descomprimir el proyecto
cd la_ultima_transmision.json

# 2. Crear entorno virtual (recomendado)
python -m venv .venv

# Windows:
.venv\Scripts\activate

# macOS / Linux:
source .venv/bin/activate

# 3. Instalar dependencias de prueba
pip install -r requirements.txt
```

---

## Ejecutar la historia principal

```bash
python cli.py
# o indicando la ruta explícita:
python cli.py historias/la_ultima_transmision.json
```

Durante el juego se muestran las opciones numeradas. Comandos disponibles:

| Tecla | Acción |
|---|---|
| `1`, `2`, … | Elegir la opción numerada |
| `d` | Deshacer la última decisión (solo aparece si está disponible) |
| `r` | Reiniciar la partida desde el inicio |
| `q` | Salir |

---

## Rutas para demostrar los tres finales

### Final E4 — Rescate (conoce el origen y activa con código)
```
E1: Revisar señal → E2
E2: Investigar archivo → E3   (conoce_origen = verdadero)
E3: Activar con código → E4   (condición: conoce_origen = verdadero)
```

### Final E5 — El eco (activa sin verificar)
```
E1: Revisar señal → E2
E2: Continuar sin investigar → E3   (conoce_origen = falso)
E3: Activar sin verificar → E5     (condición: conoce_origen = falso)
```

### Final E6 — Silencio (corta la comunicación)
```
E1: Revisar señal → E2
E2: Investigar archivo o Continuar sin investigar → E3
E3: Cortar comunicación → E6   (sin condición)
```

---

## Cargar una segunda historia

```bash
python cli.py historias/segunda_historia.json
```

Esto demuestra que el motor es genérico: se carga "El faro apagado" (4 escenas,
1 variable `tiene_luz`) sin modificar ningún archivo de `motor/` ni `cli.py`.

---

## Ejecutar las pruebas automatizadas

```bash
# Todas las pruebas (48 en total)
python -m pytest tests/ -v

# Solo las pruebas unitarias de sesión
python -m pytest tests/test_sesion.py -v

# Solo las pruebas de la función deshacer (RF15-RF19)
python -m pytest tests/test_deshacer.py -v

# Solo las pruebas de validación de contenido
python -m pytest tests/test_validacion.py -v

# Solo las pruebas de confiabilidad (RNF03)
python -m pytest tests/test_rnf.py -v

# Solo las pruebas de la segunda historia (RNF01)
python -m pytest tests/test_segunda_historia.py -v
```

La salida esperada es `48 passed` en menos de 1 segundo. Los registros de
ejecución están en `docs/resultados_pruebas.txt` (v1, 23 pruebas),
`docs/resultados_pruebas_v2.txt` (v2, 33 pruebas) y
`docs/resultados_pruebas_v3.txt` (v3 final, 48 pruebas).

---

## Formato del archivo de historia (JSON)

```json
{
  "titulo": "Nombre de la historia",
  "inicio": "ID_escena_inicial",
  "variables": {
    "nombre_variable": false
  },
  "escenas": [
    {
      "id": "E1",
      "texto": "Texto que ve el lector.",
      "final": false,
      "opciones": [
        {
          "id": "opcion_id",
          "texto": "Texto de la opción",
          "destino": "E2",
          "condiciones": {},
          "efectos": {"nombre_variable": true}
        }
      ]
    },
    {
      "id": "E2",
      "texto": "Escena final.",
      "final": true,
      "opciones": []
    }
  ]
}
```

**Reglas del formato:**
- `condiciones` vacío → opción siempre habilitada
- `efectos` vacío → no cambia variables
- Solo se admiten valores booleanos (`true` / `false`) en variables, condiciones y efectos
- Las escenas finales (`"final": true`) deben tener `"opciones": []`
- Las escenas no finales deben tener al menos una opción

---

## Limitaciones conocidas

- Solo se soporta un nivel de retroceso (deshacer la última decisión, no varias)
- Las condiciones solo admiten igualdad exacta sobre booleanos (no hay `>`, `<`, `!=` ni expresiones)
- No se guarda el progreso entre ejecuciones
- No hay soporte para audio, imágenes ni interfaz gráfica
- No se detectan automáticamente todos los callejones sin salida posibles en el grafo de escenas;
  el bloqueo se informa en tiempo de ejecución si ocurre

---

## Estructura del proyecto

```
├── cli.py                          # Interfaz de consola
├── requirements.txt                # Dependencias (pytest)
├── README.md                       # Este archivo
├── historias/
│   ├── la_ultima_transmision.json  # Historia principal (6 escenas)
│   └── segunda_historia.json       # Historia de demostración RNF01 (4 escenas)
├── motor/
│   ├── modelos.py                  # Estructuras de datos (Historia, Escena, Opcion)
│   ├── cargador.py                 # Lectura, validación y construcción
│   ├── sesion.py                   # Estado de la partida
│   └── errores.py                  # Excepciones propias
├── tests/
│   ├── conftest.py                 # Fixtures compartidas
│   ├── test_sesion.py              # U1-U5
│   ├── test_deshacer.py            # U6, U5 e I1 extendidas
│   ├── test_validacion.py          # U4 (10 variantes de error)
│   ├── test_integracion.py         # I1, CA01-CA03
│   ├── test_rnf.py                 # RNF03
│   └── test_segunda_historia.py    # RNF01
└── docs/
    ├── requisitos.md
    ├── arquitectura.md
    ├── modelos.md
    ├── proceso.md
    ├── cambio.md
    ├── trazabilidad.md
    ├── evidencia_rnf01.txt
    └── resultados_pruebas_v3.txt
```
