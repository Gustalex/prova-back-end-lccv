from django.db import models


class AbstractBaseModel(models.Model):
    """
    Modelo que fornece uma abstracao para os outros modelos para campos em comum
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
