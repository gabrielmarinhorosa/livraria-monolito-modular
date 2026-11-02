"""PAGAMENTO · camada de APLICAÇÃO — rotas REST em /api/pagamento."""
from flask import Blueprint, jsonify, request

from modulos.comum import ErroNegocio

from . import negocio

bp = Blueprint("pagamento", __name__, url_prefix="/api/pagamento")


@bp.post("/compras")
def finalizar():
    """Corpo: {"usuario_id": 1, "metodo": "pix", "itens": [{"livro_id": 1, "quantidade": 2}]}"""
    d = request.get_json(silent=True) or {}
    itens = {}
    try:
        for item in d.get("itens") or []:
            livro_id = int(item["livro_id"])
            itens[livro_id] = itens.get(livro_id, 0) + int(item["quantidade"])
    except (TypeError, KeyError, ValueError):
        raise ErroNegocio("Itens inválidos.")
    compra = negocio.finalizar_compra(d.get("usuario_id"), itens, d.get("metodo"))
    return jsonify(compra), 201


@bp.get("/compras")
def listar():
    return jsonify(negocio.listar_compras(request.args.get("usuario_id", type=int)))
