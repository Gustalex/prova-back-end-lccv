from rest_framework import serializers

from ..models import Colaborador


class ColaboradorSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo Colaborador
    """

    class Meta:
        model = Colaborador
        fields = "__all__"
        read_only_fields = ["id"]
