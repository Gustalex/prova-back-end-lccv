from django.contrib import admin

from .models import (
    AvaliacaoDesempenho,
    ItemAvaliacaoDesempenho,
    StatusAvaliacao,
    TipoItemAvaliacaoDesempenho,
)


@admin.register(TipoItemAvaliacaoDesempenho)
class TipoItemAvaliacaoDesempenhoAdmin(admin.ModelAdmin):
    """
    Configuração do admin para o modelo TipoItemAvaliacaoDesempenho.
    """

    list_display = ("tipo_item_avaliacao_desempenho", "dimensao", "descricao")
    list_filter = ("dimensao",)
    search_fields = ("tipo_item_avaliacao_desempenho", "descricao")
    ordering = ("dimensao", "tipo_item_avaliacao_desempenho")

    fieldsets = (
        (
            "Informações do Tipo",
            {
                "fields": (
                    "tipo_item_avaliacao_desempenho",
                    "dimensao",
                    "descricao",
                )
            },
        ),
    )


class ItemAvaliacaoDesempenhoInline(admin.TabularInline):
    """
    Inline para editar itens de avaliação dentro da avaliação.
    """

    model = ItemAvaliacaoDesempenho
    extra = 0
    fields = ("tipo_item_avaliacao_desempenho", "nota", "observacoes")
    readonly_fields = ("tipo_item_avaliacao_desempenho",)
    can_delete = False

    def has_add_permission(self, request, obj=None):
        """Impede a adição de novos itens inline."""
        return False


@admin.register(AvaliacaoDesempenho)
class AvaliacaoDesempenhoAdmin(admin.ModelAdmin):
    """
    Configuração do admin para o modelo AvaliacaoDesempenho.
    """

    list_display = (
        "colaborador",
        "supervisor",
        "mes_competencia",
        "status_avaliacao",
        "nota",
    )
    list_filter = ("status_avaliacao", "mes_competencia")
    search_fields = (
        "colaborador__nome",
        "supervisor__nome",
    )
    ordering = ("-mes_competencia", "colaborador__nome")
    date_hierarchy = "mes_competencia"
    inlines = [ItemAvaliacaoDesempenhoInline]
    actions = ["action_iniciar", "action_dar_feedback", "action_concluir"]

    fieldsets = (
        (
            "Informações da Avaliação",
            {
                "fields": (
                    "colaborador",
                    "supervisor",
                    "mes_competencia",
                )
            },
        ),
        (
            "Status e Nota",
            {
                "fields": ("status_avaliacao", "nota"),
                "classes": ("wide",),
            },
        ),
        (
            "Feedback",
            {
                "fields": (
                    "sugestoes_supervisor",
                    "observacoes_avaliado",
                ),
                "classes": ("wide",),
            },
        ),
    )

    readonly_fields = ("status_avaliacao", "nota")

    def save_formset(self, request, form, formset, change):
        """
        Atualiza a nota da avaliação após salvar os itens inline.
        """
        instances = formset.save(commit=False)
        for instance in instances:
            instance.save()
        formset.save_m2m()

        if change and formset.model == ItemAvaliacaoDesempenho:
            form.instance.atualizar_nota()

    @admin.action(description="Iniciar avaliação")
    def action_iniciar(self, request, queryset):
        """Inicia avaliações em massa."""
        count = 0
        for avaliacao in queryset:
            if avaliacao.status_avaliacao == StatusAvaliacao.CRIADA:
                avaliacao.iniciar()
                count += 1
        self.message_user(request, f"{count} avaliação(ões) iniciada(s) com sucesso.")

    @admin.action(description="Dar feedback")
    def action_dar_feedback(self, request, queryset):
        """Registra feedback em avaliações em massa."""
        count = 0
        for avaliacao in queryset:
            if avaliacao.status_avaliacao == StatusAvaliacao.EM_ELABORACAO:
                avaliacao.dar_feedback()
                count += 1
        self.message_user(
            request, f"{count} avaliação(ões) movida(s) para 'Em avaliação'."
        )

    @admin.action(description="Concluir avaliação")
    def action_concluir(self, request, queryset):
        """Conclui avaliações em massa."""
        count = 0
        for avaliacao in queryset:
            if avaliacao.status_avaliacao == StatusAvaliacao.EM_AVALIACAO:
                avaliacao.concluir()
                count += 1
        self.message_user(request, f"{count} avaliação(ões) concluída(s) com sucesso.")


@admin.register(ItemAvaliacaoDesempenho)
class ItemAvaliacaoDesempenhoAdmin(admin.ModelAdmin):
    """
    Configuração do admin para o modelo ItemAvaliacaoDesempenho.
    """

    list_display = (
        "avaliacao",
        "tipo_item_avaliacao_desempenho",
        "nota",
    )
    list_filter = (
        "tipo_item_avaliacao_desempenho__dimensao",
        "nota",
    )
    search_fields = (
        "avaliacao__colaborador__nome",
        "tipo_item_avaliacao_desempenho__tipo_item_avaliacao_desempenho",
    )
    ordering = ("avaliacao", "tipo_item_avaliacao_desempenho")

    fieldsets = (
        (
            "Avaliação",
            {"fields": ("avaliacao",)},
        ),
        (
            "Item",
            {
                "fields": (
                    "tipo_item_avaliacao_desempenho",
                    "nota",
                    "observacoes",
                )
            },
        ),
    )

    readonly_fields = ("avaliacao", "tipo_item_avaliacao_desempenho")

    def save_model(self, request, obj, form, change):
        """
        Atualiza a nota da avaliação após salvar o item.
        """
        super().save_model(request, obj, form, change)
        if change:
            obj.avaliacao.atualizar_nota()
