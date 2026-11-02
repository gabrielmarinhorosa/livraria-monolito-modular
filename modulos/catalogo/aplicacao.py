"""CATÁLOGO · camada de APLICAÇÃO — rotas REST em /api/catalogo."""
from flask import Blueprint, jsonify, request

from . import negocio

bp = Blueprint("catalogo", __name__, url_prefix="/api/catalogo")


@bp.get("/livros")
def listar():
    return jsonify(negocio.listar())


@bp.post("/livros")
def cadastrar():
    d = request.get_json(silent=True) or {}
    livro = negocio.cadastrar(d.get("titulo"), d.get("autor"), d.get("preco"))
    return jsonify(livro), 201
