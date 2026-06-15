from django.contrib import admin
from django.utils.html import format_html
from .models import Profesor


@admin.register(Profesor)
class ProfesorAdmin(admin.ModelAdmin):
    list_display = (
        "miniaturas",
        "usuario",
        "especialidad",
        "telefono",
    )
    search_fields = (
        "usuario__username",
        "usuario__first_name",
        "usuario__last_name",
        "especialidad",
    )
    list_filter = ("especialidad",)
    ordering = ("usuario__last_name",)

    def miniaturas(self, obj):
        if obj.miniatura:
            return format_html('<img src="{}" width="50"/>', obj.miniatura.url)
        return "-"

    miniaturas.short_description = "Foto"
