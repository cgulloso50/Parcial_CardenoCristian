from motor.errores import ErrorJugada


class Sesion:
    def __init__(self, historia):
        self._historia = historia
        self.reiniciar()

    def reiniciar(self):
        self._escena_id = self._historia.inicio
        self._variables = dict(self._historia.variables)

    @property
    def escena_actual(self):
        return self._historia.escenas[self._escena_id]

    @property
    def variables(self):
        return dict(self._variables)  # copia: nadie la modifica desde fuera

    def _habilitada(self, opcion):
        return all(self._variables[v] == val for v, val in opcion.condiciones.items())

    def opciones_disponibles(self):
        return [o for o in self.escena_actual.opciones if self._habilitada(o)]

    def esta_finalizada(self):
        return self.escena_actual.final

    def esta_bloqueada(self):
        return not self.esta_finalizada() and not self.opciones_disponibles()

    def elegir(self, id_opcion):
        existentes = {o.id: o for o in self.escena_actual.opciones}
        if id_opcion not in existentes:
            raise ErrorJugada(f"La opción '{id_opcion}' no existe en la escena '{self._escena_id}'")
        opcion = existentes[id_opcion]
        if not self._habilitada(opcion):
            raise ErrorJugada(f"La opción '{id_opcion}' no está disponible con el estado actual")
        # Solo se modifica el estado cuando todo ya fue validado
        self._variables.update(opcion.efectos)
        self._escena_id = opcion.destino
