"""Entidades del dominio de pedidos

En este archivo usted encontrará las entidades del dominio de pedidos

"""

from __future__ import annotations
from dataclasses import dataclass, field

import aeroalpes.modulos.pedidos.dominio.objetos_valor as ov
from aeroalpes.modulos.pedidos.dominio.eventos import OrdenCreada, OrdenAprobada, OrdenCancelada, OrdenPagada
from aeroalpes.seedwork.dominio.entidades import Locacion, AgregacionRaiz, Entidad

@dataclass
class Direccion(Locacion):
    codigo: ov.Codigo = field(default_factory=ov.Codigo)
    nombre: ov.NombreBarrio = field(default_factory=ov.NombreBarrio)

    def __str__(self) -> str:
        return self.codigo.codigo.upper()

@dataclass
class Ubicacion(Entidad):
    codigo: ov.Codigo = field(default_factory=ov.Codigo)
    nombre: ov.NombreBarrio = field(default_factory=ov.NombreBarrio)
    rutas: list[ov.Ruta] = field(default_factory=list[ov.Ruta])

    def obtener_rutas(self, odos: list[Odo], parametros: ParametroBusca):
        return self.rutas

@dataclass
class Paquete(Entidad):
    clase: ov.Clase = field(default_factory=ov.Clase)
    tipo: ov.TipoPaquete = field(default_factory=ov.TipoPaquete)

@dataclass
class Orden(AgregacionRaiz):
    id_cliente: uuid.UUID = field(hash=True, default=None)
    estado: ov.EstadoOrden = field(default=ov.EstadoOrden.PENDIENTE)
    rutas: list[ov.Ruta] = field(default_factory=list[ov.Ruta])

    def crear_orden(self, orden: Orden):
        self.id_cliente = orden.id_cliente
        self.estado = orden.estado
        self.rutas = orden.rutas

        self.agregar_evento(OrdenCreada(id_orden=self.id, id_cliente=self.id_cliente, estado=self.estado.name, fecha_creacion=self.fecha_creacion))

    def aprobar_orden(self):
        self.estado = ov.EstadoOrden.APROBADA

        self.agregar_evento(OrdenAprobada(self.id, self.fecha_actualizacion))

    def cancelar_orden(self):
        self.estado = ov.EstadoOrden.CANCELADA

        self.agregar_evento(OrdenCancelada(self.id, self.fecha_actualizacion))
    
    def pagar_orden(self):
        self.estado = ov.EstadoOrden.PAGADA

        self.agregar_evento(OrdenPagada(self.id, self.fecha_actualizacion))
