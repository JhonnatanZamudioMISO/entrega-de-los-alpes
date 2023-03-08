from __future__ import annotations
from dataclasses import dataclass, field
from aeroalpes.seedwork.dominio.eventos import (EventoDominio)
from datetime import datetime

@dataclass
class OrdenCreada(EventoDominio):
    id_orden: uuid.UUID = None
    id_cliente: uuid.UUID = None
    estado: str = None
    fecha_creacion: datetime = None
    
@dataclass
class OrdenCancelada(EventoDominio):
    id_orden: uuid.UUID = None
    fecha_actualizacion: datetime = None

@dataclass
class OrdenAprobada(EventoDominio):
    id_orden: uuid.UUID = None
    fecha_actualizacion: datetime = None

@dataclass
class OrdenPagada(EventoDominio):
    id_orden: uuid.UUID = None
    fecha_actualizacion: datetime = None