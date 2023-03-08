import aeroalpes.seedwork.presentacion.api as api
import json
from aeroalpes.modulos.pedidos.aplicacion.servicios import ServicioOrden
from aeroalpes.modulos.pedidos.aplicacion.dto import OrdenDTO
from aeroalpes.seedwork.dominio.excepciones import ExcepcionDominio

from flask import redirect, render_template, request, session, url_for
from flask import Response
from aeroalpes.modulos.pedidos.aplicacion.mapeadores import MapeadorOrdenDTOJson
from aeroalpes.modulos.pedidos.aplicacion.comandos.crear_reserva import CrearReserva
from aeroalpes.modulos.pedidos.aplicacion.queries.obtener_reserva import ObtenerReserva
from aeroalpes.seedwork.aplicacion.comandos import ejecutar_commando
from aeroalpes.seedwork.aplicacion.queries import ejecutar_query

bp = api.crear_blueprint('pedidos', '/pedidos')

@bp.route('/orden', methods=('POST',))
def orden():
    try:
        orden_dict = request.json

        map_orden = MapeadorOrdenDTOJson()
        orden_dto = map_orden.externo_a_dto(orden_dict)

        sr = ServicioOrden()
        dto_final = sr.crear_orden(orden_dto)

        return map_orden.dto_a_externo(dto_final)
    except ExcepcionDominio as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')

@bp.route('/orden-comando', methods=('POST',))
def orden_asincrona():
    try:
        orden_dict = request.json

        map_orden = MapeadorOrdenDTOJson()
        orden_dto = map_orden.externo_a_dto(orden_dict)

        comando = CrearOrden(orden_dto.fecha_creacion, orden_dto.fecha_actualizacion, orden_dto.id, orden_dto.rutas)
        
        # TODO Reemplaze es todo código sincrono y use el broker de eventos para propagar este comando de forma asíncrona
        # Revise la clase Despachador de la capa de infraestructura
        ejecutar_commando(comando)
        
        return Response('{}', status=202, mimetype='application/json')
    except ExcepcionDominio as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')

@bp.route('/orden', methods=('GET',))
@bp.route('/orden/<id>', methods=('GET',))
def dar_orden(id=None):
    if id:
        sr = ServicioOrden()
        map_orden = MapeadorOrdenDTOJson()
        
        return map_orden.dto_a_externo(sr.obtener_orden_por_id(id))
    else:
        return [{'message': 'GET!'}]

@bp.route('/orden-query', methods=('GET',))
@bp.route('/orden-query/<id>', methods=('GET',))
def dar_orden_usando_query(id=None):
    if id:
        query_resultado = ejecutar_query(ObtenerOrden(id))
        map_orden = MapeadorOrdenDTOJson()
        
        return map_orden.dto_a_externo(query_resultado.resultado)
    else:
        return [{'message': 'GET!'}]