from aeroalpes.seedwork.aplicacion.comandos import Comando
from aeroalpes.modulos.pedidos.aplicacion.dto import RutaDTO, OrdenDTO
from .base import CrearOrdenBaseHandler
from dataclasses import dataclass, field
from aeroalpes.seedwork.aplicacion.comandos import ejecutar_commando as comando

from aeroalpes.modulos.pedidos.dominio.entidades import Orden
from aeroalpes.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from aeroalpes.modulos.pedidos.aplicacion.mapeadores import MapeadorOrden
from aeroalpes.modulos.pedidos.infraestructura.repositorios import RepositorioOrdenes

@dataclass
class CrearOrden(Comando):
    fecha_creacion: str
    fecha_actualizacion: str
    id: str
    rutas: list[RutaDTO]


class CrearOrdenHandler(CrearOrdenBaseHandler):
    
    def handle(self, comando: CrearOrden):
        orden_dto = OrdenDTO(
                fecha_actualizacion=comando.fecha_actualizacion
            ,   fecha_creacion=comando.fecha_creacion
            ,   id=comando.id
            ,   rutas=comando.rutas)

        orden: Orden = self.fabrica_pedidos.crear_objeto(orden_dto, MapeadorOrden())
        orden.crear_orden(orden)

        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioOrdenes.__class__)

        UnidadTrabajoPuerto.registrar_batch(repositorio.agregar, orden)
        UnidadTrabajoPuerto.savepoint()
        UnidadTrabajoPuerto.commit()


@comando.register(CrearOrden)
def ejecutar_comando_crear_orden(comando: CrearOrden):
    handler = CrearOrdenHandler()
    handler.handle(comando)
    