"""Ponto de entrada do monolito modular.

Um único processo Flask que registra as rotas de cada módulo e o front-end.
Faz o papel do "API Gateway / BFF" do diagrama 8.2: é a única porta de entrada.
"""
import os

from flask import Flask, jsonify

import web
from modulos import catalogo, estoque, pagamento, usuarios
from modulos.comum import ErroNegocio

MODULOS = (catalogo, usuarios, estoque, pagamento)


def criar_app():
    app = Flask(__name__)
    app.secret_key = os.environ.get("SECRET_KEY", "dev-livraria")
    app.json.ensure_ascii = False

    for modulo in MODULOS:
        app.register_blueprint(modulo.iniciar())
    app.register_blueprint(web.bp)

    @app.errorhandler(ErroNegocio)
    def erro_negocio(e):
        return jsonify(erro=str(e)), e.status

    return app


app = criar_app()

if __name__ == "__main__":
    app.run(debug=True)
