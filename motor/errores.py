class ErrorMotor(Exception):
    """Base de los errores controlados del motor."""


class ErrorContenido(ErrorMotor):
    """El archivo de la historia no es válido. Guarda todos los problemas."""

    def __init__(self, errores):
        self.errores = list(errores)
        super().__init__("\n".join(self.errores))


class ErrorJugada(ErrorMotor):
    """La acción pedida durante la partida no es válida."""
