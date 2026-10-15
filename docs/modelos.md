# Modelos – La última transmisión (v2)

**Integrante:** Cristian David Cardeño Gulloso

---

## 1. Diagrama de contexto

El sistema Motor de Historias Interactivas recibe un archivo de historia de la escritora y expone una interfaz de consola al lector. La coordinadora del festival también interactúa indirectamente al revisar los mensajes de error de validación.

```mermaid
flowchart LR
    ES["✏️ Escritora\n(edita archivos JSON)"]
    DI["🎨 Diseñador\n(define condiciones\ny efectos)"]
    LE["👤 Lector\n(juega la historia)"]
    CO["📋 Coordinadora\n(recibe diagnósticos\nde error)"]

    subgraph SIS["Motor de Historias Interactivas"]
        CLI["cli.py\n(consola)"]
        MOT["motor/\n(reglas)"]
        DAT["historias/*.json\n(contenido)"]
    end

    ES -->|"archivos JSON"| DAT
    DI -->|"condiciones y efectos\nen el JSON"| DAT
    LE -->|"elige opciones\npor consola"| CLI
    CLI -->|"texto de escenas\ny opciones"| LE
    CLI -->|"mensajes de error\nde contenido"| CO
```

---

## 2. Casos de uso

```mermaid
flowchart LR
    ES["✏️ Escritora"]
    LE["👤 Lector"]
    CO["📋 Coordinadora"]

    CU1(["Cargar historia\ndesde archivo"])
    CU2(["Ver escena\ny opciones"])
    CU3(["Elegir opción"])
    CU4(["Deshacer\núltima decisión"])
    CU5(["Reiniciar partida"])
    CU6(["Reconocer final"])
    CU7(["Recibir diagnóstico\nde error"])

    ES --> CU1
    LE --> CU2
    LE --> CU3
    LE --> CU4
    LE --> CU5
    LE --> CU6
    CO --> CU7
    CU1 -->|"«include»"| CU7
    CU3 -->|"«include»"| CU2
    CU4 -->|"«extend»"| CU3
```

**Descripción de casos de uso:**

| ID | Nombre | Actor principal | Descripción breve |
|---|---|---|---|
| CU1 | Cargar historia | Escritora / Sistema | Lee el JSON, valida todos los campos y construye la Historia. Si hay errores los reporta todos y no abre sesión. |
| CU2 | Ver escena y opciones | Lector | Muestra el texto de la escena actual y solo las opciones cuyas condiciones se cumplen. |
| CU3 | Elegir opción | Lector | Valida que la opción exista y esté habilitada; aplica efectos y avanza al destino. |
| CU4 | Deshacer última decisión | Lector | Restaura la escena y variables anteriores a la última elección válida (un nivel). |
| CU5 | Reiniciar partida | Lector | Vuelve a la escena inicial con las variables originales y elimina el historial. |
| CU6 | Reconocer final | Lector | Al llegar a una escena final, muestra el texto y el mensaje "FIN de la historia". |
| CU7 | Recibir diagnóstico | Coordinadora | Cada error de validación indica causa, campo e ID involucrado. |

---

## 3. Clases del dominio

```mermaid
classDiagram
    class Historia {
        +str titulo
        +str inicio
        +dict variables
        +dict escenas
    }

    class Escena {
        +str id
        +str texto
        +bool final
        +tuple opciones
    }

    class Opcion {
        +str id
        +str texto
        +str destino
        +dict condiciones
        +dict efectos
    }

    class Sesion {
        -str _escena_id
        -dict _variables
        -tuple _previo
        +escena_actual() Escena
        +variables() dict
        +opciones_disponibles() list
        +elegir(id_opcion)
        +deshacer()
        +puede_deshacer() bool
        +esta_finalizada() bool
        +esta_bloqueada() bool
        +reiniciar()
    }

    class ErrorMotor {
        <<exception>>
    }

    class ErrorContenido {
        <<exception>>
        +list errores
    }

    class ErrorJugada {
        <<exception>>
    }

    Historia "1" --> "1..*" Escena : contiene
    Escena "1" --> "0..*" Opcion : tiene
    Opcion --> Escena : destino
    Sesion --> Historia : usa
    Sesion --> Escena : escena_actual
    ErrorMotor <|-- ErrorContenido
    ErrorMotor <|-- ErrorJugada
```

> [!NOTE]
> `Historia`, `Escena` y `Opcion` son `dataclass(frozen=True)`: inmutables. `Sesion` es la única clase con estado mutable de la partida. `ErrorContenido` acumula todos los errores encontrados en la lista `errores`.

---

## 4. Diagrama de secuencia — Elegir una opción

```mermaid
sequenceDiagram
    actor Lector
    participant CLI as cli.py
    participant Sesion as Sesion
    participant Escena as Escena (actual)
    participant ErrorJugada as ErrorJugada

    Lector->>CLI: ingresa número de opción
    CLI->>Sesion: opciones_disponibles()
    Sesion->>Escena: consulta opciones
    Escena-->>Sesion: lista de Opcion
    Sesion-->>CLI: opciones habilitadas

    CLI->>Sesion: elegir(id_opcion)
    Sesion->>Escena: verifica existencia de id_opcion
    alt opción no existe
        Sesion-->>ErrorJugada: raise ErrorJugada
        ErrorJugada-->>CLI: excepción
        CLI-->>Lector: "Entrada no válida" (estado intacto)
    else opción existe pero no habilitada
        Sesion-->>ErrorJugada: raise ErrorJugada
        ErrorJugada-->>CLI: excepción
        CLI-->>Lector: mensaje de error (estado intacto)
    else opción válida y habilitada
        Sesion->>Sesion: guarda _previo = (escena_id, variables)
        Sesion->>Sesion: aplica efectos en _variables
        Sesion->>Sesion: avanza _escena_id al destino
        Sesion-->>CLI: éxito
        CLI-->>Lector: muestra nueva escena y opciones
    end
```

---

## 5. Diagrama de estados — Sesion

```mermaid
stateDiagram-v2
    [*] --> EnCurso: iniciar (sin retroceso disponible)

    EnCurso --> EnCurso: elegir opción válida\n(guarda estado previo)
    EnCurso --> Finalizada: destino es escena final
    EnCurso --> Bloqueada: escena no final\nsin opciones habilitadas

    Finalizada --> EnCurso: deshacer\n(restaura estado previo)
    Bloqueada --> EnCurso: deshacer\n(restaura estado previo)
    EnCurso --> EnCurso: deshacer\n(restaura estado previo)

    Finalizada --> EnCurso: reiniciar\n(borra historial)
    Bloqueada --> EnCurso: reiniciar\n(borra historial)
    EnCurso --> EnCurso: reiniciar\n(borra historial)

    EnCurso --> EnCurso: elegir inválido\n(estado intacto, _previo intacto)
```

---

## 6. Coherencia entre modelos y requisitos

| Modelo | Requisitos que refleja |
|---|---|
| Contexto | N01–N06 (todos los actores y el sistema completo) |
| Casos de uso | RF01, RF04–RF07, RF10–RF11, RF15, RF12–RF13 |
| Clases | RF01–RF03 (Historia/Escena/Opcion), RF05–RF09 (Sesion), RF12 (ErrorContenido) |
| Secuencia de elegir | RF05–RF07, RF18 (estado intacto ante error) |
| Estados | RF10, RF11, RF14, RF15–RF17, RF19 |
