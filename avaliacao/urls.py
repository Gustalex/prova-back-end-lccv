from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    AvaliacaoDesempenhoViewset,
    ItemAvaliacaoDesempenhoViewset,
    TipoItemAvaliacaoDesempenhoViewset,
)

router = DefaultRouter()
router.register(
    r"avaliacoes-desempenho",
    AvaliacaoDesempenhoViewset,
    basename="avaliacao-desempenho",
)
router.register(
    r"itens-avaliacao-desempenho",
    ItemAvaliacaoDesempenhoViewset,
    basename="item-avaliacao-desempenho",
)
router.register(
    r"tipos-itens-avaliacao-desempenho",
    TipoItemAvaliacaoDesempenhoViewset,
    basename="tipo-item-avaliacao-desempenho",
)

urlpatterns = [
    path("", include(router.urls)),
]
