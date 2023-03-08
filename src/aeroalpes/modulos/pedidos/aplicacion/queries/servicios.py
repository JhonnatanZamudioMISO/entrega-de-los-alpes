from aeroalpes.seedwork.aplicacion.servicios import Servicio
from aeroalpes.modulos.pedidos.dominio.entidades import Orden
from aeroalpes.modulos.pedidos.dominio.fabricas import FabricaPedidos
from aeroalpes.modulos.pedidos.infraestructura.fabricas import FabricaRepositorio
from aeroalpes.modulos.pedidos.infraestructura.repositorios import RepositorioOrdenes
from aeroalpes.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from .mapeadores import MapeadorOrden

from .dto import OrdenDTO

import asyncio

class ServicioOrden(Servicio):

    def __init__(self):
        self._fabrica_repositorio: FabricaRepositorio = FabricaRepositorio()
        self._fabrica_pedidos: FabricaPedidos = FabricaPedidos()

    @property
    def fabrica_repositorio(self):
        return self._fabrica_repositorio
    
    @property
    def fabrica_pedidos(self):
        return self._fabrica_pedidos       
    
    def crear_orden(self, orden_dto: OrdenDTO) -> OrdenDTO:
        orden: Orden = self.fabrica_pedidos.crear_objeto(orden_dto, MapeadorOrden())
        orden.crear_orden(orden)

        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioOrdenes.__class__)

        UnidadTrabajoPuerto.registrar_batch(repositorio.agregar, orden)
        UnidadTrabajoPuerto.savepoint()
        UnidadTrabajoPuerto.commit()

        return self.fabrica_pedidos.crear_objeto(orden, MapeadorOrden())

    def obtener_orden_por_id(self, id) -> OrdenDTO:
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioOrdenes.__class__)
        return self.fabrica_pedidos.crear_objeto(repositorio.obtener_por_id(id), MapeadorOrden())

