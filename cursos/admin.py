from django.contrib import admin
from rangefilter.filters import DateRangeFilter
from .models import Curso
from django.utils.html import format_html
from datetime import datetime, time, timedelta
from django.utils import timezone


class FiltroFechas(admin.SimpleListFilter):
    title = "Filtro temporal"
    parameter_name = "periodo"

    def lookups(self, request, model_admin):
        return (
            ("hoy", "Hoy"),
            ("manana", "Mañana"),
            ("semana", "Esta semana"),
            ("mes", "Este mes"),
        )

    def queryset(self, request, queryset):

        hoy = timezone.localdate()

        if self.value() == "hoy":
            inicio = datetime.combine(hoy, time.min)
            fin = datetime.combine(hoy, time.max)
            return queryset.filter(fecha_inicio__range=(inicio, fin))

        if self.value() == "manana":
            d = hoy + timedelta(days=1)
            inicio = datetime.combine(d, time.min)
            fin = datetime.combine(d, time.max)
            return queryset.filter(fecha_inicio__range=(inicio, fin))

        if self.value() == "semana":
            inicio_d = hoy - timedelta(days=hoy.weekday())
            fin_d = inicio_d + timedelta(days=6)
            inicio = datetime.combine(inicio_d, time.min)
            fin = datetime.combine(fin_d, time.max)
            return queryset.filter(fecha_inicio__range=(inicio, fin))

        if self.value() == "mes":
            inicio_d = hoy.replace(day=1)
            if hoy.month == 12:
                fin_d = hoy.replace(year=hoy.year + 1, month=1, day=1)
            else:
                fin_d = hoy.replace(month=hoy.month + 1, day=1)

            return queryset.filter(fecha_inicio__gte=inicio_d, fecha_inicio__lt=fin_d)

        return queryset


@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = (
        "miniatura",
        "nombre",
        "profesor",
        "fecha_inicio",
        "fecha_fin",
        "plazas",
        "activo",
    )
    search_fields = (
        "nombre",
        "descripcion",
        "profesor__usuario__first_name",
        "profesor__usuario__last_name",
    )
    list_filter = (
        "activo",
        FiltroFechas,
    )
    ordering = ("nombre",)

    def get_rangefilter_fecha_inicio(self, request):
        return (None, datetime.date.today())

    def miniatura(self, obj):
        if obj.imagen:
            return format_html('<img src="{}" width="80"/>', obj.imagen.url)
        return "-"

    miniatura.short_description = "Imagen"

    fieldsets = (
        (
            "Información General",
            {
                "fields": (
                    "nombre",
                    "descripcion",
                    "profesor",
                )
            },
        ),
        (
            "Planificación",
            {
                "fields": (
                    "fecha_inicio",
                    "fecha_fin",
                    "plazas",
                )
            },
        ),
        (
            "Publicación",
            {
                "fields": (
                    "activo",
                    "imagen",
                )
            },
        ),
    )
