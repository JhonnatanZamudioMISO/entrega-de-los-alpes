"""Reglas de negocio del dominio de cliente

En este archivo usted encontrará reglas de negocio del dominio de cliente

"""

from aeroalpes.seedwork.dominio.reglas import ReglaNegocio
from .objetos_valor import Ruta
from .entidades import Paquete
from .objetos_valor import TipoPaquete, Ruta


class MinimoUnPaquete(ReglaNegocio):

    paquetes: list[Paquete]

    def __init__(self, paquetes, mensaje='Al menos un paquete tipo producto debe ser parte de la ruta'):
        super().__init__(mensaje)
        self.paquetes = paquetes

    def es_valido(self) -> bool:
        for paquete in self.paquetes:
            if paquete.tipo == TipoPaquete.PRODUCTO:
                return True
        return False

class RutaValida(ReglaNegocio):

    ruta: Ruta

    def __init__(self, ruta, mensaje='La ruta propuesta es incorrecta'):
        super().__init__(mensaje)
        self.ruta = ruta

    def es_valido(self) -> bool:
        return self.ruta.destino != self.ruta.origen

class MinimoUnaRuta(ReglaNegocio):
    rutas: list[Ruta]

    def __init__(self, rutas, mensaje='La lista de rutas debe tener al menos una ruta'):
        super().__init__(mensaje)
        self.rutas = rutas

    def es_valido(self) -> bool:
        return len(self.rutas) > 0 and isinstance(self.rutas[0], Ruta) 