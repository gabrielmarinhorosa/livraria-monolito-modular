"""Módulo CATÁLOGO — interface pública.

Regra do monolito modular: outros módulos só usam o que está neste arquivo,
nunca importam `negocio` ou `dados` direto. Se o módulo virar microsserviço,
estas funções viram chamadas HTTP.
"""
from . import negocio
from .aplicacao import bp
from .negocio import cadastrar as cadastrar_livro
from .negocio import listar as listar_livros
from .negocio import obter as obter_livro


def iniciar():
    negocio.carregar_iniciais()
    return bp
