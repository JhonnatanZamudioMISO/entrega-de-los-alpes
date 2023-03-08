""" Fábricas para la creación de objetos en la capa de infrastructura del dominio de pedidos

En este archivo usted encontrará las diferentes fábricas para crear
objetos complejos en la capa de infraestructura del dominio de pedidos

"""

from dataclasses import dataclass, field
from aeroalpes.seedwork.dominio.fabricas import Fabrica
from aeroalpes.seedwork.dominio.repositorios import Repositorio
from aeroalpes.modulos.pedidos.dominio.repositorios import RepositorioUbicaciones, RepositorioOrdenes
from .repositorios import RepositorioOrdenesSQLite, RepositorioUbicacionesSQLite
from .excepciones import ExcepcionFabrica

@dataclass
class FabricaRepositorio(Fabrica):
    def crear_objeto(self, obj: type, mapeador: any = None) -> Repositorio:
        if obj == RepositorioOrdenes.__class__:
            return RepositorioOrdenesSQLite()
        elif obj == RepositorioUbicaciones.__class__:
            return RepositorioUbicacionesSQLite()
        else:
            raise ExcepcionFabrica()