from django.contrib import admin

from .models import Colaborador


@admin.register(Colaborador)
class ColaboradorAdmin(admin.ModelAdmin):
    """
    Configuração do admin para o modelo Colaborador.
    """

    list_display = ("nome", "cpf", "email")
    search_fields = ("nome", "email", "cpf")
    ordering = ("nome",)

    fieldsets = (
        (
            "Informações do Colaborador",
            {"fields": ("nome", "cpf", "email")},
        ),
        (
            "Auditoria",
            {
                "fields": ("created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )

    readonly_fields = ("created_at", "updated_at")
