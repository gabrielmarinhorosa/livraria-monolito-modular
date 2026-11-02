"""USUÁRIOS · camada de APLICAÇÃO — rotas REST em /api/usuarios."""
from flask import Blueprint, jsonify, request

from . import negocio

bp = Blueprint("usuarios", __name__, url_prefix="/api/usuarios")


@bp.get("")
def listar():
    return jsonify(negocio.listar())


@bp.post("")
def cadastrar():
    d = request.get_json(silent=True) or {}
    return jsonify(negocio.cadastrar(d.get("nome"), d.get("email"))), 201
