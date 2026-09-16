from django.shortcuts import render
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from main.models import Experience
from main.models import Project
from main.forms import ProjectForm  

def show_main(request):
    context = {
        "name": "Kevin Nicholas Santoso",
        "npm": "2506637041",
        "study_program": "S1 KKI Ilmu Komputer",
        "bio": (
            "CS student at Universital Indonesia International Class. "
            "Part time artist drawing animals in their free time."
        ),
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Kevin Nicholas Santoso",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)

def project_list(request):

    json_response = get_projects_json(request)

    projects = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    projects = [obj.object for obj in projects]
    title_query = request.GET.get("title", "").strip()
    context = {
        'name': 'Kevin Nicholas Santoso',
        'project_list': projects,
        'title_query': title_query,
    }
    return render(request, "projects.html", context)

def create_project(request):
    form = ProjectForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek baru berhasil ditambahkan!")
        return redirect("main:project_list")

    context = {
        "name": "Burhan",
        "form": form,
    }
    return render(request, "projects_form.html", context)

def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    projects_json = serializers.serialize("json", projects)
    return HttpResponse(projects_json, content_type="application/json")

def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        project.delete()
        messages.success(request, "Project berhasil dihapus!")
        return redirect("main:project_list")

    return redirect("main:project_list")