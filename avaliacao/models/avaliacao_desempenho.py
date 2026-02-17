from auditlog.registry import auditlog
from django.db import models, transaction

from colaborador.models import Colaborador

from .abstract_base_model import AbstractBaseModel
from .status_avaliacao import StatusAvaliacao
from .tipo_item_avaliacao_desempenho import TipoItemAvaliacaoDesempenho


class AvaliacaoDesempenho(AbstractBaseModel):
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

    def save(self, *args, **kwargs):
        """
        Sobrescreve o método save para criar os itens de avaliação quando uma nova avaliação é criada.
        """
        nova_avaliacao = self.pk is None
        super().save(*args, **kwargs)

        if nova_avaliacao:
            from .item_avaliacao_desempenho import ItemAvaliacaoDesempenho

            with transaction.atomic():
                tipos = TipoItemAvaliacaoDesempenho.objects.all()
                itens_para_criar = [
                    ItemAvaliacaoDesempenho(
                        avaliacao=self,
                        tipo_item_avaliacao_desempenho=tipo,
                        nota=1,
                    )
                    for tipo in tipos
                ]
                ItemAvaliacaoDesempenho.objects.bulk_create(itens_para_criar)

    def atualizar_nota(self):
        """
        (soma das notas dos itens) / (total de tipos de itens * 5) * 100
        """
        with transaction.atomic():
            itens = self.itens.all()
            total_tipos = TipoItemAvaliacaoDesempenho.objects.count()

            if total_tipos > 0:
                soma_notas = sum(item.nota for item in itens)
                self.nota = (soma_notas / (total_tipos * 5)) * 100
                self.save(update_fields=["nota"])

    def iniciar(self):
        """
        Inicia a avaliação, mudando o status para Em elaboração.
        """
        if self.status_avaliacao == StatusAvaliacao.CRIADA:
            self.status_avaliacao = StatusAvaliacao.EM_ELABORACAO
            self.save()

    def dar_feedback(self):
        """
        Atualiza o status da avaliacao iniciada para Em avaliação.
        """
        if self.status_avaliacao == StatusAvaliacao.EM_ELABORACAO:
            self.status_avaliacao = StatusAvaliacao.EM_AVALIACAO
            self.save()

    def concluir(self):
        """
        Conclui a avaliação, mudando o status para Concluída.
        """
        if self.status_avaliacao == StatusAvaliacao.EM_AVALIACAO:
            self.status_avaliacao = StatusAvaliacao.CONCLUIDA
            self.save()


auditlog.register(AvaliacaoDesempenho)
