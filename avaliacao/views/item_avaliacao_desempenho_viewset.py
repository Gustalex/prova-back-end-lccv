from rest_framework import viewsets
from rest_framework.exceptions import ValidationError

from ..models import ItemAvaliacaoDesempenho, StatusAvaliacao
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

    def perform_update(self, serializer):
        """
        Sobrescreve o método de atualizar para validar o status e recalcular a nota da avaliação quando um item é editado.
        """
        item = self.get_object()

        status_permitidos = [StatusAvaliacao.EM_ELABORACAO]
        if item.avaliacao.status_avaliacao not in status_permitidos:
            raise ValidationError(
                f"Não é possível atualizar itens de uma avaliação com status '{item.avaliacao.status_avaliacao}'."
            )

        item = serializer.save()
        item.avaliacao.atualizar_nota()
