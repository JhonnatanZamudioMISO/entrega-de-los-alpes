from pydispatch import dispatcher
from .handlers import HandlerOrdenDominio

dispatcher.connect(HandlerOrdenDominio.handle_orden_creada, signal='OrdenCreadaDominio')
