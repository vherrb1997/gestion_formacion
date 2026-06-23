from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from cursos.models import Curso
from .models import Matricula
from django.shortcuts import render
from django.db.models import Count

from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


@login_required
def matricularse(request, curso_id):
    curso = get_object_or_404(Curso, pk=curso_id, activo=True)

    if request.user.tipo != "alumno":
        messages.error(request, "Sólo los alumnos pueden matricularse.")
        return redirect("detalle_curso", curso.id)
    inscritos = curso.matriculas.count()

    if inscritos >= curso.plazas:
        messages.error(request, "No quedan plazas.")
        return redirect("detalle_curso", curso.id)

    matricula, creada = Matricula.objects.get_or_create(
        alumno=request.user, curso=curso
    )

    if creada:
        messages.success(request, "Matrícula realizada correctamente.")
    else:
        messages.warning(request, "Ya estás matriculado en este curso.")
    return redirect("detalle_curso", curso.id)


@login_required
def mis_cursos(request):
    matriculas = Matricula.objects.filter(alumno=request.user).select_related("curso")
    return render(request, "matriculas/mis_cursos.html", {"matriculas": matriculas})


class DashboardAlumnoView(LoginRequiredMixin, TemplateView):
    template_name = "matriculas/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_matriculas"] = Matricula.objects.filter(
            alumno=self.request.user
        ).count()
        return context


@login_required
def cancelar_matricula(request, matricula_id):
    matricula = get_object_or_404(Matricula, pk=matricula_id, alumno=request.user)
    matricula.delete()
    messages.success(request, "Matrícula cancelada.")
    return redirect("mis_cursos")
