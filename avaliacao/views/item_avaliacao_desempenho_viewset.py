from rest_framework import status, viewsets
from rest_framework.response import Response

from ..models import ItemAvaliacaoDesempenho
from ..serializers import ItemAvaliacaoDesempenhoSerializer


class ItemAvaliacaoDesempenhoViewset(viewsets.ModelViewSet):
    """
    ViewSet para o modelo ItemAvaliacaoDesempenho.

    Permite apenas listar, visualizar e atualizar itens (nota e observações).
    Criação e exclusão são gerenciadas automaticamente pelo modelo AvaliacaoDesempenho.
    """

    queryset = ItemAvaliacaoDesempenho.objects.all()
    serializer_class = ItemAvaliacaoDesempenhoSerializer
    http_method_names = ["get", "post", "patch"]
