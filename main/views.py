import datetime

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from main.forms import ExperienceForm, ProjectForm
from main.models import Experience, Project
from main.permissions import permission_context, permission_required


def show_main(request):
    last_login = request.COOKIES.get("last_login", "No active login session / Cookie not found")
    context = {
        "name": "Kevin Nicholas Santoso",
        "npm": "2506637041",
        "study_program": "S1 KKI Ilmu Komputer",
        "bio": (
            "CS student at Universitas Indonesia International Class. "
            "Part time artist drawing animals in their free time."
        ),
        "last_login": last_login,
    }
    context.update(permission_context(request))
    return render(request, "index.html", context)

def show_experience(request):
    json_response = get_experience_json(request)
    experiences = serializers.deserialize("json", json_response.content.decode("utf-8"))
    experience_list = [obj.object for obj in experiences]
    context = {
        "name": "Kevin Nicholas Santoso",
        "experience_list": experience_list,
    }
    context.update(permission_context(request))
    return render(request, "experience.html", context)


def get_experience_json(request):
    experiences = Experience.objects.all()
    experiences_json = serializers.serialize(
        "json", experiences,
        fields=("title", "category", "description", "is_ongoing", "timestamp"),
    )
    return HttpResponse(experiences_json, content_type="application/json")


@permission_required(superuser_only=True)          # owner only; others get 403
def create_experience(request):
    form = ExperienceForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Pengalaman baru berhasil ditambahkan!")
        return redirect("main:show_experience")
    context = {"name": "Kevin Nicholas Santoso", "form": form}
    context.update(permission_context(request))
    return render(request, "experience_form.html", context)


@permission_required("main.change_experience")    # editor group or superuser
def update_experience(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)
    form = ExperienceForm(request.POST or None, instance=experience)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Successfully updated experience!")
        return redirect("main:show_experience")
    context = {"name": "Kevin Nicholas Santoso", "form": form, "experience": experience}
    context.update(permission_context(request))
    return render(request, "experience_form.html", context)


@permission_required(superuser_only=True)          # owner only
def delete_experience(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)
    if request.method == "POST":
        experience.delete()
        messages.success(request, "Successfully deleted experience!")
    return redirect("main:show_experience")

def project_list(request):
    json_response = get_projects_json(request)
    projects = serializers.deserialize("json", json_response.content.decode("utf-8"))
    project_list = [obj.object for obj in projects]
    context = {
        "name": "Kevin Nicholas Santoso",
        "project_list": project_list,
        "title_query": request.GET.get("title", "").strip(),
    }
    context.update(permission_context(request))
    return render(request, "projects.html", context)


def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.all()
    if title_query:
        projects = projects.filter(title__icontains=title_query)
    # Explicit field whitelist: M2M (starred_by) and any sensitive data never leak.
    projects_json = serializers.serialize(
        "json", projects, fields=("title", "description", "year"),
    )
    return HttpResponse(projects_json, content_type="application/json")


@permission_required(superuser_only=True)
def create_project(request):
    form = ProjectForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek baru berhasil ditambahkan!")
        return redirect("main:project_list")
    context = {"name": "Kevin Nicholas Santoso", "form": form}
    context.update(permission_context(request))
    return render(request, "projects_form.html", context)


@permission_required(superuser_only=True)
def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.method == "POST":
        project.delete()
        messages.success(request, "Project berhasil dihapus!")
    return redirect("main:project_list")

@permission_required("main.change_project")
def update_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    form = ProjectForm(request.POST or None, instance=project)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Successfully updated project!")
        return redirect("main:project_list")
    context = {"name": "Kevin Nicholas Santoso", "form": form, "project": project}
    context.update(permission_context(request))
    return render(request, "projects_form.html", context)


@login_required(login_url="/login/")          
def toggle_star(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.method == "POST":
        if request.user in project.starred_by.all():
            project.starred_by.remove(request.user)   
            messages.success(request, "Star removed.")
        else:
            project.starred_by.add(request.user)
            messages.success(request, "Project starred!")
    return redirect("main:project_list")

def register(request):
    form = UserCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Account created successfully. Please log in.")
        return redirect("main:login")
    context = {"name": "Kevin Nicholas Santoso", "form": form}
    context.update(permission_context(request))
    return render(request, "register.html", context)


def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        response = redirect("main:show_main")
        response.set_cookie("last_login", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        return response
    context = {"name": "Kevin Nicholas Santoso", "form": form}
    context.update(permission_context(request))
    return render(request, "login.html", context)


def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie("last_login")
    return response