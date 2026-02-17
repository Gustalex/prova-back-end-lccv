from rest_framework import filters, viewsets

from ..models import TipoItemAvaliacaoDesempenho
from ..serializers import TipoItemAvaliacaoDesempenhoSerializer


class TipoItemAvaliacaoDesempenhoViewset(viewsets.ModelViewSet):
    """
    ViewSet para o modelo TipoItemAvaliacaoDesempenho, disponibiliza operaçoes de CRUD.
    """

    queryset = TipoItemAvaliacaoDesempenho.objects.all()
    serializer_class = TipoItemAvaliacaoDesempenhoSerializer
    http_method_names = ["get", "post", "patch"]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["tipo_item_avaliacao_desempenho", "descricao"]
    ordering_fields = ["dimensao", "tipo_item_avaliacao_desempenho", "created_at"]
    ordering = ["dimensao", "tipo_item_avaliacao_desempenho"]
