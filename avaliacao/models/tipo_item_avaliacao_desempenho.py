from auditlog.registry import auditlog
from django.db import models

from .abstract_base_model import AbstractBaseModel
from .dimensao_item_avaliacao import DimensaoItemAvaliacao


class TipoItemAvaliacaoDesempenho(AbstractBaseModel):
    """
    Modelo para representar os tipos de itens de avaliação de desempenho, como comportamento, entregas e trabalho em equipe.
    """

    dimensao = models.CharField(
        max_length=20,
        choices=DimensaoItemAvaliacao.choices,
    )
    tipo_item_avaliacao_desempenho = models.CharField(max_length=50)
    descricao = models.TextField()

    class Meta:
        verbose_name = "Tipo de Item de Avaliação de Desempenho"
        verbose_name_plural = "Tipos de Itens de Avaliação de Desempenho"
        ordering = ["dimensao", "tipo_item_avaliacao_desempenho"]

    def __str__(self):
        return f"{self.dimensao} - {self.tipo_item_avaliacao_desempenho}"


auditlog.register(TipoItemAvaliacaoDesempenho)
