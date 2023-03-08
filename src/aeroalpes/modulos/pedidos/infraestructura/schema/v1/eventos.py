from pulsar.schema import *
from aeroalpes.seedwork.infraestructura.schema.v1.eventos import EventoIntegracion

class OrdenCreadaPayload(Record):
    id_orden = String()
    id_cliente = String()
    estado = String()
    fecha_creacion = Long()

class EventoOrdenCreada(EventoIntegracion):
    data = OrdenCreadaPayload()