from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from ..models import AvaliacaoDesempenho, StatusAvaliacao
from ..serializers import (
    AtualizarNotaSerializer,
    AvaliacaoDesempenhoSerializer,
    ConcluirAvaliacaoSerializer,
    DarFeedbackSerializer,
    IniciarAvaliacaoSerializer,
)


class AvaliacaoDesempenhoViewset(viewsets.ModelViewSet):
    """
    ViewSet para o modelo AvaliacaoDesempenho, disponibiliza operaçoes de CRUD.
    """

    queryset = AvaliacaoDesempenho.objects.all()
    serializer_class = AvaliacaoDesempenhoSerializer
    http_method_names = ["get", "post", "patch"]

    def get_serializer_class(self):
        """Retorna o serializer apropriado para cada action."""
        if self.action == "iniciar_avaliacao":
            return IniciarAvaliacaoSerializer
        if self.action == "dar_feedback_avaliacao":
            return DarFeedbackSerializer
        if self.action == "concluir_avaliacao":
            return ConcluirAvaliacaoSerializer
        if self.action == "atualizar_nota":
            return AtualizarNotaSerializer
        return super().get_serializer_class()

    def perform_update(self, serializer):
        """
        Sobrescreve o método de atualizar para checar o status da avaliação antes de permitir a edição.
        """
        avaliacao = self.get_object()
        serializer.save()

        status_permitidos = [
            StatusAvaliacao.EM_ELABORACAO,
            StatusAvaliacao.EM_AVALIACAO,
        ]
        if avaliacao.status_avaliacao not in status_permitidos:
            raise ValidationError(
                f"Não é possível atualizar uma avaliação com status '{avaliacao.status_avaliacao}'."
            )

    @action(detail=True, methods=["POST"], url_path="iniciar-avaliacao")
    def iniciar_avaliacao(self, request, pk=None):
        """
        Inicia uma avaliação desempenho.
        """
        avaliacao = self.get_object()
        avaliacao.iniciar()

        serializer = self.get_serializer(avaliacao)
        return Response(
            {"message": "Avaliação iniciada com sucesso", "data": serializer.data},
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["POST"], url_path="dar-feedback")
    def dar_feedback_avaliacao(self, request, pk=None):
        """
        Registra o feedback do supervisor e muda o status para Em avaliação.
        """
        avaliacao = self.get_object()
        avaliacao.dar_feedback()

        serializer = self.get_serializer(avaliacao)
        return Response(
            {"message": "Feedback registrado com sucesso", "data": serializer.data},
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["POST"], url_path="concluir-avaliacao")
    def concluir_avaliacao(self, request, pk=None):
        """
        Conclui uma avaliação desempenho.
        """
        avaliacao = self.get_object()
        avaliacao.concluir()

        serializer = self.get_serializer(avaliacao)
        return Response(
            {"message": "Avaliação concluída com sucesso", "data": serializer.data},
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["POST"], url_path="atualizar-nota")
    def atualizar_nota(self, request, pk=None):
        """
        Recalcula a nota da avaliação baseado nas notas dos itens.
        """
        avaliacao = self.get_object()

        status_permitidos = [StatusAvaliacao.EM_ELABORACAO]
        if avaliacao.status_avaliacao not in status_permitidos:
            raise ValidationError(
                f"Não é possível atualizar uma avaliação com status '{avaliacao.status_avaliacao}'."
            )

        avaliacao.atualizar_nota()

        serializer = self.get_serializer(avaliacao)
        return Response(
            {"message": "Nota atualizada com sucesso", "data": serializer.data},
            status=status.HTTP_200_OK,
        )
