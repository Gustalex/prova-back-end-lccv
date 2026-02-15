from auditlog.registry import auditlog
from django.db import models

from .abstrat_model import AbstractBaseModel


class Colaborador(AbstractBaseModel):
    """
    Modelo simples para representar um colaborador, com campos básicos como nome, CPF e email.
    """

    nome = models.CharField(max_length=50)
    cpf = models.CharField(max_length=11, unique=True)
    email = models.EmailField(unique=True)

    class Meta:
        verbose_name = "Colaborador"
        verbose_name_plural = "Colaboradores"
        ordering = ["nome"]

    def __str__(self):
        return self.nome


auditlog.register(Colaborador)
