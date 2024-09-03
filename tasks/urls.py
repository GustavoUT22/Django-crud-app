from django.urls import path
from . import views

urlpatterns = [
    path("tasks/", views.tasks, name="tasks"),
    path("", views.index, name="index"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.session, name="login"),
    path("profile/", views.profile, name="profile"),
    path("logout/ ", views.close_sesion, name="logout"),
    path("tasks/create/", views.create_task, name="create_task"),
]
