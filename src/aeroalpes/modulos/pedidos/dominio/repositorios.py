""" Interfaces para los repositorios del dominio de pedidos

En este archivo usted encontrará las diferentes interfaces para repositorios
del dominio de pedidos

"""

from abc import ABC
from aeroalpes.seedwork.dominio.repositorios import Repositorio

class RepositorioOrdenes(Repositorio, ABC):
    ...

class RepositorioUbicaciones(Repositorio, ABC):
    ...