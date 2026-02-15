from django.db import models


class DimensaoItemAvaliacao(models.TextChoices):
    """
    Modelo para representar as dimensões de avaliação, como comportamento, entregas e trabalho em equipe.
    """

    COMPORTAMENTO = "COMPORTAMENTO", "Comportamento"
    ENTREGAS = "ENTREGAS", "Entregas"
    TRABALHO_EM_EQUIPE = "TRABALHO_EM_EQUIPE", "Trabalho em Equipe"
