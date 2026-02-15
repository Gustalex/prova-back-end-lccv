from django.db import models


class StatusAvaliacao(models.TextChoices):
    """
    Modelo para representar os status de uma avaliação, como criada, em elaboração, em avaliação e concluída.
    """

    CRIADA = "CRIADA", "Criada"
    EM_ELABORACAO = "EM_ELABORACAO", "Em Elaboração"
    EM_AVALIACAO = "EM_AVALIACAO", "Em Avaliação"
    CONCLUIDA = "CONCLUIDA", "Concluída"
