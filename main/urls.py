from django.urls import path

from main.views import show_main, show_experience
from main.views import project_list
from main.views import create_project, get_projects_json, delete_project
from main.views import get_experience_json, create_experience, update_experience, delete_experience

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experience/", show_experience, name="show_experience"),
    path('projects/', project_list, name='project_list'),
    path("projects/add/", create_project, name="create_project"),
    path("api/projects/", get_projects_json, name="get_projects_json"),
    path("projects/<int:project_id>/delete/", delete_project, name="delete_project"),
    path("experience/json/", get_experience_json, name="get_experience_json"),
    path("experience/create/", create_experience, name="create_experience"),
    path("experience/update/<int:experience_id>/", update_experience, name="update_experience"),
    path("experience/delete/<int:experience_id>/", delete_experience, name="delete_experience"),
]
