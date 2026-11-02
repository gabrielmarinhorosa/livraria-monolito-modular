"""ESTOQUE · camada de NEGÓCIO — consulta, ajuste e baixa de estoque.

O estoque só conhece o id do livro e a quantidade; título e preço são do catálogo.
"""
from modulos.comum import ErroNegocio

from . import dados

# Quantidades iniciais dos 4 livros que o catálogo carrega (ids 1 a 4).
ESTOQUE_INICIAL = {1: 5, 2: 3, 3: 8, 4: 2}


def carregar_iniciais():
    dados.limpar()
    for livro_id, qtd in ESTOQUE_INICIAL.items():
        dados.definir(livro_id, qtd)


def listar():
    return [{"livro_id": i, "quantidade": q} for i, q in dados.listar().items()]


def consultar(livro_id):
    return dados.obter(livro_id)


def definir(livro_id, quantidade):
    try:
        quantidade = int(quantidade)
    except (TypeError, ValueError):
        raise ErroNegocio("Quantidade inválida.")
    if quantidade < 0:
        raise ErroNegocio("Quantidade não pode ser negativa.")
    dados.definir(livro_id, quantidade)
    return quantidade


def baixar(itens):
    """Baixa {livro_id: quantidade}. Tudo ou nada: confere todos antes de baixar."""
    for livro_id, qtd in itens.items():
        if qtd <= 0:
            raise ErroNegocio("Quantidade deve ser maior que zero.")
        if dados.obter(livro_id) < qtd:
            raise ErroNegocio(f"Estoque insuficiente para o livro {livro_id}.", 409)
    for livro_id, qtd in itens.items():
        dados.definir(livro_id, dados.obter(livro_id) - qtd)
