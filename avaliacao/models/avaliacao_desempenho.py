from auditlog.registry import auditlog
from django.db import models

from colaborador.models import Colaborador

from .status_avaliacao import StatusAvaliacao


class AvaliacaoDesempenho(models.Model):
    """
    Modelo para avaliacao de desempenho dos colaboradores

        - colaborador: O colaborador que está sendo avaliado.
        - supervisor: O supervisor responsável pela avaliação.
        - mes_competencia: O mês e ano da competência avaliada.
        - status_avaliacao: O status atual da avaliação (Criada, Em elaboracao, Em avaliacao, Concluída).
        - nota: Nota final da avaliação
        - sugestoes_supervisor: Sugestões do supervisor.
        - observacoes_avaliado: Observações do colaborador.

    """

    colaborador = models.ForeignKey(
        Colaborador, on_delete=models.CASCADE, related_name="avaliacoes"
    )
    supervisor = models.ForeignKey(
        Colaborador, on_delete=models.CASCADE, related_name="supervisoes"
    )
    mes_competencia = models.DateField()
    status_avaliacao = models.CharField(
        max_length=20, choices=StatusAvaliacao.choices, default=StatusAvaliacao.CRIADA
    )
    nota = models.FloatField(default=0.0)
    sugestoes_supervisor = models.TextField(blank=True, null=True)
    observacoes_avaliado = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ("colaborador", "mes_competencia")
        verbose_name = "Avaliação de Desempenho"
        verbose_name_plural = "Avaliações de Desempenho"
        ordering = ["-mes_competencia"]

    def __str__(self):
        return f"Avaliação de {self.colaborador} - {self.mes_competencia.strftime('%m/%Y')} - Status: {self.status_avaliacao}"


auditlog.register(AvaliacaoDesempenho)
