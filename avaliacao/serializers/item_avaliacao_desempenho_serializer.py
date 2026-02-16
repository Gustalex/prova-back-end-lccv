from rest_framework import serializers

from ..models import ItemAvaliacaoDesempenho


class ItemAvaliacaoDesempenhoSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo ItemAvaliacaoDesempenho
    """

    class Meta:
        model = ItemAvaliacaoDesempenho
        fields = "__all__"
        read_only_fields = ["id", "avaliacao", "tipo_item_avaliacao_desempenho"]
