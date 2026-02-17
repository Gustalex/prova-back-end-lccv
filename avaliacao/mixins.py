from rest_framework.exceptions import ValidationError

from .constants import (
    MSG_ERRO_STATUS_INVALIDO_ATUALIZACAO,
    MSG_ERRO_STATUS_INVALIDO_ITEM,
)


class ValidacaoStatusAvaliacaoMixin:
    """
    Mixin para validar status de avaliação antes de permitir atualizações.
    """

    def validar_status_avaliacao(self, avaliacao, status_permitidos):
        """
        Valida se a avaliação está em um dos status permitidos.
        """
        if avaliacao.status_avaliacao not in status_permitidos:
            raise ValidationError(
                MSG_ERRO_STATUS_INVALIDO_ATUALIZACAO.format(
                    status=avaliacao.status_avaliacao
                )
            )

    def validar_status_item_avaliacao(self, item, status_permitidos):
        """
        Valida se o item de avaliação está em um dos status permitidos.
        """
        if item.avaliacao.status_avaliacao not in status_permitidos:
            raise ValidationError(
                MSG_ERRO_STATUS_INVALIDO_ITEM.format(
                    status=item.avaliacao.status_avaliacao
                )
            )
