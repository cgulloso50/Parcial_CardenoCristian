from dataclasses import dataclass


@dataclass(frozen=True)
class Opcion:
    id: str
    texto: str
    destino: str
    condiciones: dict
    efectos: dict


@dataclass(frozen=True)
class Escena:
    id: str
    texto: str
    final: bool
    opciones: tuple


@dataclass(frozen=True)
class Historia:
    titulo: str
    inicio: str
    variables: dict
    escenas: dict  # id de escena -> Escena
