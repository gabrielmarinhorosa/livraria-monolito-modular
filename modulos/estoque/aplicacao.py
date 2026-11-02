"""ESTOQUE · camada de APLICAÇÃO — rotas REST em /api/estoque."""
from flask import Blueprint, jsonify, request

from . import negocio

bp = Blueprint("estoque", __name__, url_prefix="/api/estoque")


@bp.get("")
def listar():
    return jsonify(negocio.listar())


@bp.get("/<int:livro_id>")
def consultar(livro_id):
    return jsonify(livro_id=livro_id, quantidade=negocio.consultar(livro_id))


@bp.put("/<int:livro_id>")
def definir(livro_id):
    d = request.get_json(silent=True) or {}
    return jsonify(livro_id=livro_id, quantidade=negocio.definir(livro_id, d.get("quantidade")))
