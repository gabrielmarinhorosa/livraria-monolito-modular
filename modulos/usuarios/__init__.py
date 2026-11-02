"""Módulo USUÁRIOS — interface pública. Outros módulos só importam daqui."""
from . import negocio
from .aplicacao import bp
from .negocio import cadastrar as cadastrar_usuario
from .negocio import listar as listar_usuarios
from .negocio import obter as obter_usuario


def iniciar():
    negocio.carregar_iniciais()
    return bp
