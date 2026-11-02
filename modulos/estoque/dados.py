"""ESTOQUE · camada de DADOS — faz o papel do Estoque-DB (aqui, em memória)."""
_estoque = {}  # livro_id -> quantidade


def limpar():
    _estoque.clear()


def listar():
    return dict(_estoque)


def obter(livro_id):
    return _estoque.get(livro_id, 0)


def definir(livro_id, quantidade):
    _estoque[livro_id] = quantidade
