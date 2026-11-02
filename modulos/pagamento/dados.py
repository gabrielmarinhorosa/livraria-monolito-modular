"""PAGAMENTO · camada de DADOS — faz o papel do Pagamento-DB (aqui, em memória).

Cada compra guarda uma cópia do título e do preço no momento da compra.
"""
_compras = []


def limpar():
    _compras.clear()


def salvar(usuario_id, itens, total, metodo, status):
    compra = {"id": len(_compras) + 1, "usuario_id": usuario_id, "itens": itens,
              "total": total, "metodo": metodo, "status": status}
    _compras.append(compra)
    return compra


def listar(usuario_id=None):
    return [c for c in reversed(_compras) if usuario_id is None or c["usuario_id"] == usuario_id]
