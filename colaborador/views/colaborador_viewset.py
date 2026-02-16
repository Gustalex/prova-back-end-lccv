from rest_framework import viewsets

from ..models import Colaborador
from ..serializers import ColaboradorSerializer


class ColaboradorViewset(viewsets.ModelViewSet):
    """
    ViewSet para o modelo Colaborador, disponibiliza operaçoes de CRUD.
    """

    queryset = Colaborador.objects.all()
    serializer_class = ColaboradorSerializer
