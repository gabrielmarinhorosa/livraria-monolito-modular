"""CATÁLOGO · camada de NEGÓCIO — regras de cadastro de livros."""
from modulos.comum import ErroNegocio

from . import dados

LIVROS_INICIAIS = [
    ("Dom Casmurro", "Machado de Assis", 29.90),
    ("O Cortiço", "Aluísio Azevedo", 24.50),
    ("Vidas Secas", "Graciliano Ramos", 34.90),
    ("A Hora da Estrela", "Clarice Lispector", 27.00),
]


def carregar_iniciais():
    dados.limpar()
    for titulo, autor, preco in LIVROS_INICIAIS:
        dados.inserir(titulo, autor, preco)


def listar():
    return dados.listar()


def obter(livro_id):
    return dados.obter(livro_id)


def cadastrar(titulo, autor, preco):
    titulo, autor = (titulo or "").strip(), (autor or "").strip()
    if not titulo or not autor:
        raise ErroNegocio("Título e autor são obrigatórios.")
    try:
        preco = round(float(preco), 2)
    except (TypeError, ValueError):
        raise ErroNegocio("Preço inválido.")
    if preco < 0:
        raise ErroNegocio("Preço não pode ser negativo.")
    return dados.inserir(titulo, autor, preco)
