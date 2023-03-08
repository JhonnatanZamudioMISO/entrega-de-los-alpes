"""Objetos valor del dominio de pedidos

En este archivo usted encontrará los objetos valor del dominio de pedidos

"""

from __future__ import annotations

from dataclasses import dataclass, field
from aeroalpes.seedwork.dominio.objetos_valor import ObjetoValor, Codigo, Ruta, Locacion
from datetime import datetime
from enum import Enum

@dataclass(frozen=True)
class Codigo(Codigo):
    ...

@dataclass(frozen=True)
class CodigoProducto(Codigo):
    ...

@dataclass(frozen=True)
class NombreProveedor():
    nombre: str

@dataclass(frozen=True)
class Leg(Ruta):
    fecha_salida: datetime
    fecha_llegada: datetime
    origen: Locacion
    destino: Locacion

    def origen(self) -> Locacion:
        return self.origen

    def destino(self) -> Locacion:
        return self.destino

    def fecha_salida(self) -> datetime:
        return self.fecha_salida
    
    def fecha_llegada(self) -> datetime:
        return self.fecha_llegada

@dataclass(frozen=True)
class Segmento(Ruta):
    legs: list[Leg]

    def origen(self) -> Locacion:
        return self.legs[0].origen

    def destino(self) -> Locacion:
        return self.legs[-1].destino

    def fecha_salida(self) -> datetime:
        return self.legs[0].fecha_salida
    
    def fecha_llegada(self) -> datetime:
        return self.legs[-1].fecha_llegada

class TipoEntrega(Enum):
    PUERTA_A_PUERTA = "Puerta a puerta"
    RECOGER_EN_TIENDA = "Recoger en tienda"
    PUNTO_INTERMEDIO = "Punto intermedio"

@dataclass(frozen=True)
class Ruta(ObjetoValor):
    odos: list[Odo] = field(default_factory=list)

    @classmethod
    def es_puerta_a_puerta(self) -> bool:
        return self.odos[0].origen() == self.odos[-1].destino()

    @classmethod
    def es_recoger_en_tienda(self) -> bool:
        return len(self.odos) == 1

    def tipo_entrega(self):
        if self.es_puerta_a_puerta():
            return TipoEntrega.PUERTA_A_PUERTA
        elif self.es_recoger_en_tienda:
            return TipoEntrega.RECOGER_EN_TIENDA
        else:
            return TipoVuelo.PUNTO_INTERMEDIO

    def ruta(self):
        if self.es_puerta_a_puerta():
            return f"{str(self.odos[0].origen())}-{str(self.odos[-1].origen())}"
        elif self.es_recoger_en_tienda:
            return f"{str(self.odos[0].origen())}-{str(self.odos[0].destino())}"
        else:
            return f"{str(self.odos[0].origen())}-{str(self.odos[-1].destino())}"

@dataclass(frozen=True)
class Odo(Ruta):
    segmentos: list[Segmento]

    def origen(self) -> Locacion:
        return self.segmentos[0].origen

    def destino(self) -> Locacion:
        return self.segmentos[-1].destino

    def fecha_salida(self):
        return self.segmentos[0].fecha_salida()

    def fecha_llegada(self):
        return self.segmentos[-1].fecha_llegada()

class Clase(Enum):
    ECONOMICA = "Economica"
    PREMIUM = "Premium"

class TipoPaquete(Enum):
    COMIDA = "Comida"
    TARJETA_CREDITO = "Tarjeta de credito"
    PRODUCTO = "Producto"

@dataclass(frozen=True)
class ParametroBusca(ObjetoValor):
    paquetes: list[Paquete] = field(default_factory=list)


class EstadoOrden(str, Enum):
    APROBADA = "Aprobada"
    PENDIENTE = "Pendiente"
    CANCELADA = "Cancelada"
    PAGADA = "Pagada"