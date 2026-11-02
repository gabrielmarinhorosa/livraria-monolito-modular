"""USUÁRIOS · camada de DADOS — faz o papel do User-DB (aqui, em memória)."""
_usuarios = {}


def limpar():
    _usuarios.clear()


def inserir(nome, email):
    novo_id = max(_usuarios, default=0) + 1
    _usuarios[novo_id] = {"id": novo_id, "nome": nome, "email": email}
    return dict(_usuarios[novo_id])


def listar():
    return [dict(u) for u in _usuarios.values()]


def obter(usuario_id):
    u = _usuarios.get(usuario_id)
    return dict(u) if u else None


def buscar_por_email(email):
    return next((dict(u) for u in _usuarios.values() if u["email"] == email), None)
