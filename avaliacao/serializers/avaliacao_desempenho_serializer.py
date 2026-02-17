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


class EmptyActionSerializer(serializers.Serializer):
    """
    Serializer vazio para actions que não requerem campos no body.

    Usado para melhorar a documentação do Swagger.
    """

    pass
