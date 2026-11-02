"""Módulo PAGAMENTO — interface pública. Outros módulos só importam daqui."""
from . import negocio
from .aplicacao import bp
from .negocio import finalizar_compra, listar_compras


def iniciar():
    negocio.limpar()
    return bp
