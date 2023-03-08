""" Mapeadores para la capa de infrastructura del dominio de pedidos

En este archivo usted encontrará los diferentes mapeadores
encargados de la transformación entre formatos de dominio y DTOs

"""

from aeroalpes.seedwork.dominio.repositorios import Mapeador
from aeroalpes.modulos.pedidos.dominio.objetos_valor import NombreBarrio, Odo, Leg, Segmento, Ruta, CodigoProducto
from aeroalpes.modulos.pedidos.dominio.entidades import Ubicacion, Direccion, Orden
from .dto import Orden as OrdenDTO
from .dto import Ruta as RutaDTO

class MapeadorOrden(Mapeador):
    _FORMATO_FECHA = '%Y-%m-%dT%H:%M:%SZ'

    def _procesar_ruta_dto(self, rutas_dto: list) -> list[Ruta]:
        rut_dict = dict()
        
        for rut in rutas_dto:
            destino = Direccion(codigo=rut.destino_codigo, nombre=None)
            origen = Direccion(codigo=rut.origen_codigo, nombre=None)
            fecha_salida = rut.fecha_salida
            fecha_llegada = rut.fecha_llegada

            rut_dict.setdefault(str(rut.odo_orden),{}).setdefault(str(rut.segmento_orden), {}).setdefault(str(rut.leg_orden), Leg(fecha_salida, fecha_llegada, origen, destino))

        odos = list()
        for k, odos_dict in rut_dict.items():
            segmentos = list()
            for k, seg_dict in odos_dict.items():
                legs = list()
                for k, leg in seg_dict.items():
                    legs.append(leg)
                segmentos.append(Segmento(legs))
            odos.append(Odo(segmentos))

        return [Ruta(odos)]

    def _procesar_ruta(self, ruta: any) -> list[RutaDTO]:
        rutas_dto = list()

        for i, odo in enumerate(ruta.odos):
            for j, seg in enumerate(odo.segmentos):
                for k, leg in enumerate(seg.legs):
                    ruta_dto = RutaDTO()
                    ruta_dto.destino_codigo = leg.destino.codigo
                    ruta_dto.origen_codigo = leg.origen.codigo
                    ruta_dto.fecha_salida = leg.fecha_salida
                    ruta_dto.fecha_llegada = leg.fecha_llegada
                    ruta_dto.leg_orden = k
                    ruta_dto.segmento_orden = j
                    ruta_dto.odo_orden = i

                    rutas_dto.append(ruta_dto)

        return rutas_dto

    def obtener_tipo(self) -> type:
        return Orden.__class__

    def entidad_a_dto(self, orden: Orden) -> OrdenDTO:
        
        orden_dto = OrdenDTO()
        orden_dto.fecha_creacion = entidad.fecha_creacion
        orden_dto.fecha_actualizacion = entidad.fecha_actualizacion
        orden_dto.id = str(entidad.id)

        rutas_dto = list()
        
        for ruta in entidad.rutas:
            rutas_dto.extend(self._procesar_ruta(ruta))

        orden_dto.rutas = rutas_dto

        return ruta_dto

    def dto_a_entidad(self, dto: OrdenDTO) -> Orden:
        orden = Orden(dto.id, dto.fecha_creacion, dto.fecha_actualizacion)
        orden.rutas = list()

        rutas_dto: list[RutaDTO] = dto.rutas

        orden.rutas.extend(self._procesar_ruta_dto(rutas_dto))
        
        return orden