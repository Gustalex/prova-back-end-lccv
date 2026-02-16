from rest_framework import serializers

from ..models import AvaliacaoDesempenho


class AvaliacaoDesempenhoSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo AvaliacaoDesempenho
    """

    class Meta:
        model = AvaliacaoDesempenho
        fields = "__all__"
        read_only_fields = ["id", "status_avaliacao", "nota"]


class IniciarAvaliacaoSerializer(serializers.Serializer):
    """
    Serializer vazio para iniciar avaliação.

    Este endpoint não requer nenhum campo no body.
    """

    pass


class DarFeedbackSerializer(serializers.Serializer):
    """
    Serializer vazio para registrar feedback.

    Este endpoint não requer nenhum campo no body.
    """

    pass


class ConcluirAvaliacaoSerializer(serializers.Serializer):
    """
    Serializer vazio para concluir avaliação.

    Este endpoint não requer nenhum campo no body.
    """

    pass


class AtualizarNotaSerializer(serializers.Serializer):
    """
    Serializer vazio para atualizar nota da avaliação.

    Este endpoint não requer nenhum campo no body.
    """

    pass
