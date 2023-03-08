from aeroalpes.modulos.vuelos.dominio.eventos import ReservaCreada, ReservaCancelada, ReservaAprobada, ReservaPagada
from aeroalpes.seedwork.aplicacion.handlers import Handler
from aeroalpes.modulos.vuelos.infraestructura.despachadores import Despachador

class HandlerOrdenIntegracion(Handler):

    @staticmethod
    def handle_orden_creada(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-reserva')

    @staticmethod
    def handle_orden_cancelada(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-reserva')

    @staticmethod
    def handle_orden_aprobada(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-reserva')

    @staticmethod
    def handle_orden_pagada(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-reserva')


    