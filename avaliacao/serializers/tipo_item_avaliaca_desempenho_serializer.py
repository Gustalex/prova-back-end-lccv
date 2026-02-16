from rest_framework import serializers

from ..models import TipoItemAvaliacaoDesempenho


class TipoItemAvaliacaoDesempenhoSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo TipoItemAvaliacaoDesempenho
    """

    class Meta:
        model = TipoItemAvaliacaoDesempenho
        fields = "__all__"
        read_only_fields = ["id"]
