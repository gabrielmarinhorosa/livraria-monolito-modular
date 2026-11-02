"""Código compartilhado entre os módulos."""


class ErroNegocio(Exception):
    """Regra de negócio violada. Vira uma resposta HTTP com o status informado."""

    def __init__(self, mensagem, status=400):
        super().__init__(mensagem)
        self.status = status
