from aeroalpes.seedwork.aplicacion.dto import Mapeador as AppMap
from aeroalpes.seedwork.dominio.repositorios import Mapeador as RepMap
from aeroalpes.modulos.pedidos.dominio.entidades import Orden, Direccion
from aeroalpes.modulos.pedidos.dominio.objetos_valor import Ruta, Odo, Segmento, Leg
from .dto import ReservaDTO, RutaDTO, OdoDTO, SegmentoDTO, LegDTO

from datetime import datetime

class MapeadorOrdenDTOJson(AppMap):
    def _procesar_ruta(self, ruta: dict) -> RutaDTO:
        odos_dto: list[OdoDTO] = list()
        for odo in ruta.get('odos', list()):

            segmentos_dto: list[SegmentoDTO] = list()
            for segmento in odo.get('segmentos', list()):
                legs_dto: list[LegDTO] = list()
                for leg in segmento.get('legs', list()):
                    leg_dto: LegDTO = LegDTO(leg.get('fecha_salida'), leg.get('fecha_llegada'), leg.get('origen'), leg.get('destino')) 
                    legs_dto.append(leg_dto)  
                
                segmentos_dto.append(SegmentoDTO(legs_dto))
            
            odos_dto.append(Odo(segmentos_dto))

        return RutaDTO(odos_dto)
    
    def externo_a_dto(self, externo: dict) -> OrdenDTO:
        orden_dto = OrdenDTO()

        rutas: list[RutaDTO] = list()
        for rut in externo.get('rutas', list()):
            orden_dto.rutas.append(self._procesar_ruta(rut))

        return orden_dto

    def dto_a_externo(self, dto: OrdenDTO) -> dict:
        return dto.__dict__

class MapeadorOrden(RepMap):
    _FORMATO_FECHA = '%Y-%m-%dT%H:%M:%SZ'

    def _procesar_ruta(self, ruta_dto: RutaDTO) -> Ruta:
        odos = list()

        for odo_dto in ruta_dto.odos:
            segmentos = list()
            for seg_dto in odo_dto.segmentos:
                
                legs = list()

                for leg_dto in seg_dto.legs:
                    destino = Direccion(codigo=leg_dto.destino.get('codigo'), nombre=leg_dto.destino.get('nombre'))
                    origen = Direccion(codigo=leg_dto.origen.get('codigo'), nombre=leg_dto.origen.get('nombre'))
                    fecha_salida = datetime.strptime(leg_dto.fecha_salida, self._FORMATO_FECHA)
                    fecha_llegada = datetime.strptime(leg_dto.fecha_llegada, self._FORMATO_FECHA)

                    leg: Leg = Leg(fecha_salida, fecha_llegada, origen, destino)

                    legs.append(leg)

                segmentos.append(Segmento(legs))
            
            odos.append(Odo(segmentos))

        return Ruta(odos)

    def obtener_tipo(self) -> type:
        return Orden.__class__

    def locacion_a_dict(self, locacion):
        if not locacion:
            return dict(codigo=None, nombre=None, fecha_actualizacion=None, fecha_creacion=None)
        
        return dict(
                    codigo=locacion.codigo
                ,   nombre=locacion.nombre
                ,   fecha_actualizacion=locacion.fecha_actualizacion.strftime(self._FORMATO_FECHA)
                ,   fecha_creacion=locacion.fecha_creacion.strftime(self._FORMATO_FECHA)
        )
        

    def entidad_a_dto(self, entidad: Orden) -> OrdenDTO:
        
        fecha_creacion = entidad.fecha_creacion.strftime(self._FORMATO_FECHA)
        fecha_actualizacion = entidad.fecha_actualizacion.strftime(self._FORMATO_FECHA)
        _id = str(entidad.id)
        rutas = list()

        for rut in entidad.rutas:
            odos = list()
            for odo in rut.odos:
                segmentos = list()
                for seg in odo.segmentos:
                    legs = list()
                    for leg in seg.legs:
                        fecha_salida = leg.fecha_salida.strftime(self._FORMATO_FECHA)
                        fecha_llegada = leg.fecha_llegada.strftime(self._FORMATO_FECHA)
                        origen = self.locacion_a_dict(leg.origen)
                        destino = self.locacion_a_dict(leg.destino)
                        leg = LegDTO(fecha_salida=fecha_salida, fecha_llegada=fecha_llegada, origen=origen, destino=destino)
                        
                        legs.append(leg)

                    segmentos.append(SegmentoDTO(legs))
                odos.append(OdoDTO(segmentos))
            rutas.append(RutaDTO(odos))
        
        return OrdenDTO(fecha_creacion, fecha_actualizacion, _id, rutas)

    def dto_a_entidad(self, dto: OrdenDTO) -> ORden:
        orden = Orden()
        orden.rutas = list()

        rutas_dto: list[RutaDTO] = dto.rutas

        for rut in rutas_dto:
            orden.rutas.append(self._procesar_ruta(rut))
        
        return orden



