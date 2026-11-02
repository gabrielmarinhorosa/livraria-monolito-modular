"""Módulo ESTOQUE — interface pública. Outros módulos só importam daqui."""
from . import negocio
from .aplicacao import bp
from .negocio import baixar, consultar, definir


def iniciar():
    negocio.carregar_iniciais()
    return bp
