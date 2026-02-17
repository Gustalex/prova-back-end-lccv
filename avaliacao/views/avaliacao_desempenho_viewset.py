from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from ..constants import (
    MSG_AVALIACAO_CONCLUIDA,
    MSG_AVALIACAO_INICIADA,
    MSG_FEEDBACK_REGISTRADO,
    MSG_NOTA_ATUALIZADA,
)
from ..mixins import ValidacaoStatusAvaliacaoMixin
from ..models import AvaliacaoDesempenho, StatusAvaliacao
from ..serializers import AvaliacaoDesempenhoSerializer, EmptyActionSerializer


class AvaliacaoDesempenhoViewset(ValidacaoStatusAvaliacaoMixin, viewsets.ModelViewSet):
    """
    ViewSet para o modelo AvaliacaoDesempenho, disponibiliza operaçoes de CRUD.
    """

    queryset = AvaliacaoDesempenho.objects.select_related(
        "colaborador", "supervisor"
    ).all()
    serializer_class = AvaliacaoDesempenhoSerializer
    http_method_names = ["get", "post", "patch"]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = [
        "colaborador__nome",
        "supervisor__nome",
        "colaborador__cpf",
        "supervisor__cpf",
    ]
    ordering_fields = [
        "mes_competencia",
        "status_avaliacao",
        "nota",
        "created_at",
    ]
    ordering = ["-mes_competencia"]

    def get_serializer_class(self):
        """Retorna o serializer apropriado para cada action."""
        action_serializers = [
            "iniciar_avaliacao",
            "dar_feedback_avaliacao",
            "concluir_avaliacao",
            "atualizar_nota",
        ]
        if self.action in action_serializers:
            return EmptyActionSerializer
        return super().get_serializer_class()

    def perform_update(self, serializer):
        """
        Valida o status da avaliação antes de permitir a edição.
        """
        avaliacao = self.get_object()
        status_permitidos = [
            StatusAvaliacao.EM_ELABORACAO,
            StatusAvaliacao.EM_AVALIACAO,
        ]
        self.validar_status_avaliacao(avaliacao, status_permitidos)
        serializer.save()

    @action(detail=True, methods=["POST"], url_path="iniciar-avaliacao")
    def iniciar_avaliacao(self, request, pk=None):
        """
        Inicia uma avaliação desempenho.
        """
        avaliacao = self.get_object()
        avaliacao.iniciar()

        serializer = AvaliacaoDesempenhoSerializer(avaliacao)
        return Response(
            {"message": MSG_AVALIACAO_INICIADA, "data": serializer.data},
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["POST"], url_path="dar-feedback")
    def dar_feedback_avaliacao(self, request, pk=None):
        """
        Registra o feedback do supervisor e muda o status para Em avaliação.
        """
        avaliacao = self.get_object()
        avaliacao.dar_feedback()

        serializer = AvaliacaoDesempenhoSerializer(avaliacao)
        return Response(
            {"message": MSG_FEEDBACK_REGISTRADO, "data": serializer.data},
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["POST"], url_path="concluir-avaliacao")
    def concluir_avaliacao(self, request, pk=None):
        """
        Conclui uma avaliação desempenho.
        """
        avaliacao = self.get_object()
        avaliacao.concluir()

        serializer = AvaliacaoDesempenhoSerializer(avaliacao)
        return Response(
            {"message": MSG_AVALIACAO_CONCLUIDA, "data": serializer.data},
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["POST"], url_path="atualizar-nota")
    def atualizar_nota(self, request, pk=None):
        """
        Recalcula a nota da avaliação baseado nas notas dos itens.
        """
        avaliacao = self.get_object()

        status_permitidos = [StatusAvaliacao.EM_ELABORACAO]
        self.validar_status_avaliacao(avaliacao, status_permitidos)

        avaliacao.atualizar_nota()

        serializer = AvaliacaoDesempenhoSerializer(avaliacao)
        return Response(
            {"message": MSG_NOTA_ATUALIZADA, "data": serializer.data},
            status=status.HTTP_200_OK,
        )
