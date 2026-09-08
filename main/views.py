from django.shortcuts import render

from main.models import Experience

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
