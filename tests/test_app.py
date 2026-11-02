import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import criar_app  # noqa: E402


@pytest.fixture
def cliente():
    app = criar_app()  # recarrega os dados iniciais de todos os módulos
    app.testing = True
    return app.test_client()


def estoque_de(cliente, livro_id):
    return cliente.get(f"/api/estoque/{livro_id}").get_json()["quantidade"]


def test_catalogo(cliente):
    assert len(cliente.get("/api/catalogo/livros").get_json()) == 4
    r = cliente.post("/api/catalogo/livros", json={"titulo": "Iracema", "autor": "José de Alencar", "preco": 19.9})
    assert r.status_code == 201
    assert cliente.post("/api/catalogo/livros", json={"titulo": "", "autor": "X", "preco": 1}).status_code == 400


def test_usuarios(cliente):
    assert cliente.post("/api/usuarios", json={"nome": "Ana", "email": "ana@x.com"}).status_code == 201
    assert cliente.post("/api/usuarios", json={"nome": "Ana", "email": "ana@x.com"}).status_code == 409


def test_compra_usa_preco_do_catalogo_e_baixa_estoque(cliente):
    antes = estoque_de(cliente, 1)
    r = cliente.post("/api/pagamento/compras", json={
        "usuario_id": 1, "metodo": "pix", "itens": [{"livro_id": 1, "quantidade": 2}]})
    assert r.status_code == 201
    assert r.get_json()["total"] == 59.80
    assert estoque_de(cliente, 1) == antes - 2


def test_compra_sem_estoque_nao_baixa_nada(cliente):
    r = cliente.post("/api/pagamento/compras", json={
        "usuario_id": 1, "metodo": "cartao",
        "itens": [{"livro_id": 1, "quantidade": 1}, {"livro_id": 4, "quantidade": 99}]})
    assert r.status_code == 409
    assert estoque_de(cliente, 1) == 5


def test_fluxo_pela_pagina(cliente):
    cliente.post("/carrinho/2")
    cliente.post("/carrinho/2")
    pagina = cliente.post("/comprar", data={"usuario_id": 1, "metodo": "pix"}, follow_redirects=True)
    assert "Compra #1 aprovada: R$ 49.00" in pagina.get_data(as_text=True)
    assert estoque_de(cliente, 2) == 1
