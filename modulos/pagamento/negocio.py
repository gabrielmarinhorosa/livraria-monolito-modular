"""PAGAMENTO · camada de NEGÓCIO — finalização da compra.

É o único módulo que depende de outros, e só pelas interfaces públicas deles:
  usuarios.obter_usuario -> confere se o cliente existe
  catalogo.obter_livro   -> pega o preço oficial (não confia no preço do front)
  estoque.baixar         -> tira os livros do estoque
"""
from modulos import catalogo, estoque, usuarios
from modulos.comum import ErroNegocio

from . import dados

METODOS = {"pix": "PIX", "cartao": "Cartão"}


def limpar():
    dados.limpar()


def finalizar_compra(usuario_id, itens, metodo):
    if metodo not in METODOS:
        raise ErroNegocio("Forma de pagamento inválida (use 'pix' ou 'cartao').")
    try:
        usuario_id = int(usuario_id)
    except (TypeError, ValueError):
        raise ErroNegocio("Usuário inválido.")
    if usuarios.obter_usuario(usuario_id) is None:
        raise ErroNegocio("Usuário não encontrado.", 404)
    if not itens:
        raise ErroNegocio("Carrinho vazio.")

    linhas = []
    for livro_id, qtd in itens.items():
        livro = catalogo.obter_livro(livro_id)
        if livro is None:
            raise ErroNegocio(f"Livro {livro_id} não encontrado.", 404)
        linhas.append({"livro_id": livro_id, "titulo": livro["titulo"],
                       "preco": livro["preco"], "quantidade": qtd})
    total = round(sum(l["preco"] * l["quantidade"] for l in linhas), 2)

    estoque.baixar(itens)  # levanta erro se faltar algum livro

    # Gateway PIX/cartão SIMULADO: aqui toda cobrança é aprovada.
    return dados.salvar(usuario_id, linhas, total, metodo, "aprovado")


def listar_compras(usuario_id=None):
    return dados.listar(usuario_id)
