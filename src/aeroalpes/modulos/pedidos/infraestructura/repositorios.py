""" Repositorios para el manejo de persistencia de objetos de dominio en la capa de infrastructura del dominio de pedidos

En este archivo usted encontrará las diferentes repositorios para
persistir objetos dominio (agregaciones) en la capa de infraestructura del dominio de pedidos

"""

from aeroalpes.config.db import db
from aeroalpes.modulos.pedidos.dominio.repositorios import RepositorioOrdenes, RepositorioUbicaciones
from aeroalpes.modulos.pedidos.dominio.objetos_valor import NombreBarrio, Odo, Leg, Segmento, Ruta, CodigoProducto
from aeroalpes.modulos.pedidos.dominio.entidades import Ubicacion, Direccion, Orden
from aeroalpes.modulos.pedidos.dominio.fabricas import FabricaPedidos
from .dto import Orden as OrdenDTO
from .mapeadores import MapeadorOrden
from uuid import UUID

class RepositorioUbicacionesSQLite(RepositorioUbicaciones):

    def obtener_por_id(self, id: UUID) -> Orden:
        # TODO
        raise NotImplementedError

    def obtener_todos(self) -> list[Orden]:
        origen=Direccion(codigo="110911", nombre="Calle 57a # 122 - 21")
        destino=Direccion(codigo="111146", nombre="Carrera 50a # 174b - 06")
        legs=[Leg(origen=origen, destino=destino)]
        segmentos = [Segmento(legs)]
        odos=[Odo(segmentos=segmentos)]

        ubicacion = Ubicacion(codigo=CodigoProducto(codigo="TC"), nombre=NombreBarrio(nombre= "NuevaZelandia"))
        ubicacion.rutas = [Ruta(odos=odos, ubicacion=ubicacion)]
        return [ubicacion]

    def agregar(self, entity: Orden):
        # TODO
        raise NotImplementedError

    def actualizar(self, entity: Orden):
        # TODO
        raise NotImplementedError

    def eliminar(self, entity_id: UUID):
        # TODO
        raise NotImplementedError


class RepositorioOrdenesSQLite(RepositorioOrdenes):

    def __init__(self):
        self._fabrica_pedidos: FabricaPedidos = FabricaPedidos()

    @property
    def fabrica_pedidos(self):
        return self._fabrica_pedidos

    def obtener_por_id(self, id: UUID) -> Orden:
        orden_dto = db.session.query(OrdenDTO).filter_by(id=str(id)).one()
        return self.fabrica_pedidos.crear_objeto(orden_dto, MapeadorOrden())

    def obtener_todos(self) -> list[Orden]:
        # TODO
        raise NotImplementedError

    def agregar(self, orden: Orden):
        orden_dto = self.fabrica_pedidos.crear_objeto(orden, MapeadorOrden())
        db.session.add(orden_dto)

    def actualizar(self, orden: Orden):
        # TODO
        raise NotImplementedError

    def eliminar(self, orden_id: UUID):
        # TODO
        raise NotImplementedError