from rest_framework import filters, viewsets

from ..models import Colaborador
from ..serializers import ColaboradorSerializer


class ColaboradorViewset(viewsets.ModelViewSet):
    """
    ViewSet para o modelo Colaborador, disponibiliza operaçoes de CRUD.
    """

    queryset = Colaborador.objects.all()
    serializer_class = ColaboradorSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["nome", "cpf", "email"]
    ordering_fields = ["nome", "created_at"]
    ordering = ["nome"]
