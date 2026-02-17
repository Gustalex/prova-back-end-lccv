from rest_framework import filters, viewsets

from ..mixins import ValidacaoStatusAvaliacaoMixin
from ..models import ItemAvaliacaoDesempenho, StatusAvaliacao
from ..serializers import ItemAvaliacaoDesempenhoSerializer


class ItemAvaliacaoDesempenhoViewset(
    ValidacaoStatusAvaliacaoMixin, viewsets.ModelViewSet
):
    """
    ViewSet para o modelo ItemAvaliacaoDesempenho.

    Permite apenas listar, visualizar e atualizar itens (nota e observações).
    """

    queryset = ItemAvaliacaoDesempenho.objects.select_related(
        "avaliacao",
        "tipo_item_avaliacao_desempenho",
        "avaliacao__colaborador",
    ).all()
    serializer_class = ItemAvaliacaoDesempenhoSerializer
    http_method_names = ["get", "patch", "post"]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = [
        "avaliacao__colaborador__nome",
        "tipo_item_avaliacao_desempenho__tipo_item_avaliacao_desempenho",
    ]
    ordering_fields = ["nota", "created_at"]
    ordering = [
        "tipo_item_avaliacao_desempenho__dimensao",
        "tipo_item_avaliacao_desempenho__tipo_item_avaliacao_desempenho",
    ]

    def perform_update(self, serializer):
        """
        Valida o status e recalcula a nota da avaliação quando um item é editado.
        """
        item = self.get_object()

        status_permitidos = [StatusAvaliacao.EM_ELABORACAO]
        self.validar_status_item_avaliacao(item, status_permitidos)

        item = serializer.save()
        item.avaliacao.atualizar_nota()
