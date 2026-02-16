from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ColaboradorViewset

router = DefaultRouter()
router.register(r"colaboradores", ColaboradorViewset, basename="colaborador")

urlpatterns = [
    path("", include(router.urls)),
]
