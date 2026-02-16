from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from ..models import AvaliacaoDesempenho, StatusAvaliacao
from ..serializers import AvaliacaoDesempenhoSerializer


class AvaliacaoDesempenhoViewset(viewsets.ModelViewSet):
    """
    ViewSet para o modelo AvaliacaoDesempenho, disponibiliza operaçoes de CRUD.
    """

    queryset = AvaliacaoDesempenho.objects.all()
    serializer_class = AvaliacaoDesempenhoSerializer
    http_method_names = ["get", "post", "patch"]

    @action(detail=True, methods=["POST"], url_path="transicao-status")
    def mudar_status_transicao_avaliacao(self, request, pk=None):
        """
        Muda o status da AvaliacaoDesempenho de acordo com a transição definida na máquina de estados.

        Body: {"action": "iniciar" | "dar_feedback" | "concluir"}
        """
        avaliacao = self.get_object()
        acao = request.data.get("action")

        if not acao:
            return Response(
                {"error": "Campo 'action' é obrigatório."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        transicoes = {
            StatusAvaliacao.CRIADA: {
                "iniciar": (avaliacao.iniciar, "Avaliação iniciada"),
            },
            StatusAvaliacao.EM_ELABORACAO: {
                "dar_feedback": (avaliacao.dar_feedback, "Feedback registrado"),
            },
            StatusAvaliacao.EM_AVALIACAO: {
                "concluir": (avaliacao.concluir, "Avaliação concluída"),
            },
        }

        if avaliacao.status_avaliacao not in transicoes:
            return Response(
                {
                    "error": f"Status '{avaliacao.status_avaliacao}' não permite mudanças de status."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        acoes_validas = transicoes[avaliacao.status_avaliacao]

        if acao not in acoes_validas:
            return Response(
                {
                    "error": f"Ação inválida. Status atual: '{avaliacao.status_avaliacao}'."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        metodo, mensagem = acoes_validas[acao]
        metodo()

        serializer = self.get_serializer(avaliacao)
        return Response(
            {"message": mensagem, "data": serializer.data}, status=status.HTTP_200_OK
        )

    @action(detail=True, methods=["POST"], url_path="atualizar-nota")
    def atualizar_nota(self, request, pk=None):
        """
        Recalcula a nota da avaliação baseado nas notas dos itens.
        """
        avaliacao = self.get_object()
        avaliacao.atualizar_nota()

        serializer = self.get_serializer(avaliacao)
        return Response(
            {"message": "Nota atualizada com sucesso", "data": serializer.data},
            status=status.HTTP_200_OK,
        )
