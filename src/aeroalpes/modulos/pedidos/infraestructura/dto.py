"""DTOs para la capa de infrastructura del dominio de vuelos

En este archivo usted encontrará los DTOs (modelos anémicos) de
la infraestructura del dominio de vuelos

"""

from aeroalpes.config.db import db
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, ForeignKey, Integer, Table

import uuid

Base = db.declarative_base()

# Tabla intermedia para tener la relación de muchos a muchos entre la tabla ordenes y rutas
ordenes_rutas = db.Table(
    "ordenes_rutas",
    db.Model.metadata,
    db.Column("orden_id", db.String, db.ForeignKey("ordenes.id")),
    db.Column("odo_orden", db.Integer),
    db.Column("segmento_orden", db.Integer),
    db.Column("leg_orden", db.Integer),
    db.Column("fecha_salida", db.DateTime),
    db.Column("fecha_llegada", db.DateTime),
    db.Column("origen_codigo", db.String),
    db.Column("destino_codigo", db.String),
    db.ForeignKeyConstraint(
        ["odo_orden", "segmento_orden", "leg_orden", "fecha_salida", "fecha_llegada", "origen_codigo", "destino_codigo"],
        ["rutas.odo_orden", "rutas.segmento_orden", "rutas.leg_orden", "rutas.fecha_salida", "rutas.fecha_llegada", "rutas.origen_codigo", "rutas.destino_codigo"]
    )
)

class Ruta(db.Model):
    __tablename__ = "rutas"
    odo_orden = db.Column(db.Integer, primary_key=True, nullable=False)
    segmento_orden = db.Column(db.Integer, primary_key=True, nullable=False)
    leg_orden = db.Column(db.Integer, primary_key=True, nullable=False)
    fecha_salida = db.Column(db.DateTime, nullable=False, primary_key=True)
    fecha_llegada = db.Column(db.DateTime, nullable=False, primary_key=True)
    origen_codigo = db.Column(db.String, nullable=False, primary_key=True)
    destino_codigo= db.Column(db.String, nullable=False, primary_key=True)


class Orden(db.Model):
    __tablename__ = "ordenes"
    id = db.Column(db.String, primary_key=True)
    fecha_creacion = db.Column(db.DateTime, nullable=False)
    fecha_actualizacion = db.Column(db.DateTime, nullable=False)
    rutas = db.relationship('Ruta', secondary=ordenes_rutas, backref='ordenes')
