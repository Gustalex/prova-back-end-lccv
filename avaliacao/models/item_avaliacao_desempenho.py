from auditlog.registry import auditlog
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .avaliacao_desempenho import AvaliacaoDesempenho
from .tipo_item_avaliacao_desempenho import TipoItemAvaliacaoDesempenho


class ItemAvaliacaoDesempenho(models.Model):
    """
    Modelo para representar os itens de avaliacão de desempenho que estão relacionados a um tipo de item de avaliação de desempenho.
    """

    avaliacao = models.ForeignKey(
        AvaliacaoDesempenho,
        on_delete=models.CASCADE,
        related_name="itens",
    )

    tipo_item_avaliacao_desempenho = models.ForeignKey(
        TipoItemAvaliacaoDesempenho,
        on_delete=models.PROTECT,
        related_name="tipos",
    )
    nota = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ]
    )
    observacoes = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Item de Avaliação de Desempenho"
        verbose_name_plural = "Itens de Avaliação de Desempenho"
        ordering = [
            "tipo_item_avaliacao_desempenho__dimensao",
            "tipo_item_avaliacao_desempenho__tipo_item_avaliacao_desempenho",
        ]

    def __str__(self):
        return f"{self.tipo_item_avaliacao_desempenho} - Nota: {self.nota}"


auditlog.register(ItemAvaliacaoDesempenho)
