from django.urls import path
from .views import matricularse, mis_cursos, DashboardAlumnoView, cancelar_matricula

urlpatterns = [
    path("matricular/<int:curso_id>/", matricularse, name="matricularse"),
    path("mis-cursos/", mis_cursos, name="mis_cursos"),
    path("dashboard/", DashboardAlumnoView.as_view(), name="dashboard"),
    path("cancelar/<int:matricula_id>/", cancelar_matricula, name="cancelar_matricula"),
]
