"""USUÁRIOS · camada de NEGÓCIO — cadastro de clientes."""
from modulos.comum import ErroNegocio

from . import dados


def carregar_iniciais():
    dados.limpar()
    dados.inserir("Cliente Demo", "cliente@livraria.dev")


def listar():
    return dados.listar()


def obter(usuario_id):
    return dados.obter(usuario_id)


def cadastrar(nome, email):
    nome, email = (nome or "").strip(), (email or "").strip().lower()
    if not nome:
        raise ErroNegocio("Nome é obrigatório.")
    if "@" not in email or "." not in email.split("@")[-1]:
        raise ErroNegocio("E-mail inválido.")
    if dados.buscar_por_email(email):
        raise ErroNegocio("Já existe um usuário com esse e-mail.", 409)
    return dados.inserir(nome, email)
