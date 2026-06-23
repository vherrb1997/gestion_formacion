from django.urls import path
from .views import ListaCursosView, CursoDetailView

urlpatterns = [
    path("", ListaCursosView.as_view(), name="lista_cursos"),
    path("<slug:slug>/", CursoDetailView.as_view(), name="detalle_curso"),
]
