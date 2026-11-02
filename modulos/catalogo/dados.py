"""CATÁLOGO · camada de DADOS — faz o papel do Items-DB (aqui, em memória)."""
_livros = {}


def limpar():
    _livros.clear()


def inserir(titulo, autor, preco):
    novo_id = max(_livros, default=0) + 1
    _livros[novo_id] = {"id": novo_id, "titulo": titulo, "autor": autor, "preco": preco}
    return dict(_livros[novo_id])


def listar():
    return [dict(livro) for livro in _livros.values()]


def obter(livro_id):
    livro = _livros.get(livro_id)
    return dict(livro) if livro else None
