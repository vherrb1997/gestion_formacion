from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from cursos.models import Curso
from .models import Matricula
from django.shortcuts import render
from django.db.models import Count


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


@login_required
def dashboard(request):
    total_matriculas = Matricula.objects.filter(alumno=request.user).count()
    ultima_matricula = (
        Matricula.objects.filter(alumno=request.user)
        .select_related("curso")
        .order_by("-fecha_matricula")[:5]
    )

    proximo_curso = (
        Curso.objects.filter(matriculas__alumno=request.user)
        .order_by("fecha_inicio")
        .first()
    )

    cursos_disponibles = Curso.objects.filter(activo=True).count()

    ultimas_matriculas = (
        Matricula.objects.filter(alumno=request.user)
        .select_related("curso")
        .order_by("-fecha_matricula")[:5]
    )
    return render(
        request,
        "matriculas/dashboard.html",
        {
            "total_matriculas": total_matriculas,
            "ultima_matricula": ultima_matricula,
            "proximo_curso": proximo_curso,
            "cursos_disponibles": cursos_disponibles,
            "ultimas_matriculas": ultimas_matriculas,
        },
    )


@login_required
def cancelar_matricula(request, matricula_id):
    matricula = get_object_or_404(Matricula, pk=matricula_id, alumno=request.user)
    matricula.delete()
    messages.success(request, "Matrícula cancelada.")
    return redirect("mis_cursos")
