"""FRONT-END / BFF — monta a página com as seções Catálogo, Carrinho e Compra.

Conversa com os módulos só pelas interfaces públicas deles. O carrinho fica na
sessão do navegador, como no micro-frontend "Carrinho" do diagrama.
"""
from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from modulos import catalogo, estoque, pagamento, usuarios
from modulos.comum import ErroNegocio

bp = Blueprint("web", __name__)


def _carrinho():
    """Carrinho da sessão como {livro_id: quantidade}."""
    return {int(k): v for k, v in session.get("carrinho", {}).items()}


def _salvar_carrinho(carrinho):
    session["carrinho"] = {str(k): v for k, v in carrinho.items()}


@bp.get("/")
def index():
    livros = [{**l, "estoque": estoque.consultar(l["id"])} for l in catalogo.listar_livros()]
    itens = []
    for livro_id, qtd in _carrinho().items():
        livro = catalogo.obter_livro(livro_id)
        if livro:
            itens.append({**livro, "quantidade": qtd, "subtotal": livro["preco"] * qtd})
    return render_template(
        "index.html",
        livros=livros,
        carrinho=itens,
        total=sum(i["subtotal"] for i in itens),
        usuarios=usuarios.listar_usuarios(),
        nomes={u["id"]: u["nome"] for u in usuarios.listar_usuarios()},
        compras=pagamento.listar_compras(),
    )


@bp.post("/livros")
def cadastrar_livro():
    f = request.form
    try:
        livro = catalogo.cadastrar_livro(f.get("titulo"), f.get("autor"), f.get("preco"))
        estoque.definir(livro["id"], f.get("quantidade") or 0)
        flash(f"Livro “{livro['titulo']}” cadastrado.")
    except ErroNegocio as e:
        flash(str(e), "erro")
    return redirect(url_for("web.index"))


@bp.post("/carrinho/<int:livro_id>")
def adicionar_ao_carrinho(livro_id):
    carrinho = _carrinho()
    if carrinho.get(livro_id, 0) + 1 > estoque.consultar(livro_id):
        flash("Não há mais unidades desse livro em estoque.", "erro")
    else:
        carrinho[livro_id] = carrinho.get(livro_id, 0) + 1
        _salvar_carrinho(carrinho)
    return redirect(url_for("web.index"))


@bp.post("/carrinho/limpar")
def limpar_carrinho():
    session.pop("carrinho", None)
    return redirect(url_for("web.index"))


@bp.post("/usuarios")
def cadastrar_usuario():
    try:
        u = usuarios.cadastrar_usuario(request.form.get("nome"), request.form.get("email"))
        flash(f"Cliente {u['nome']} cadastrado.")
    except ErroNegocio as e:
        flash(str(e), "erro")
    return redirect(url_for("web.index"))


@bp.post("/comprar")
def comprar():
    try:
        compra = pagamento.finalizar_compra(
            request.form.get("usuario_id"), _carrinho(), request.form.get("metodo")
        )
        session.pop("carrinho", None)
        flash(f"Compra #{compra['id']} aprovada: R$ {compra['total']:.2f}.")
    except ErroNegocio as e:
        flash(str(e), "erro")
    return redirect(url_for("web.index"))
