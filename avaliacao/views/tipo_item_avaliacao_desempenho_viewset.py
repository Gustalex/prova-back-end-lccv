from rest_framework import viewsets

from ..models import TipoItemAvaliacaoDesempenho
from ..serializers import TipoItemAvaliacaoDesempenhoSerializer


class TipoItemAvaliacaoDesempenhoViewset(viewsets.ModelViewSet):
    """
    ViewSet para o modelo TipoItemAvaliacaoDesempenho, disponibiliza operaçoes de CRUD.
    """

    queryset = TipoItemAvaliacaoDesempenho.objects.all()
    serializer_class = TipoItemAvaliacaoDesempenhoSerializer
    http_method_names = ["get", "post", "patch"]
