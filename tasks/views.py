from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import TaskForm
from .models import Task
from .forms import ProfileForm
from .models import Profile


def signup(request):
    if request.user.is_authenticated:
        return redirect("tasks")  # Redirigir si el usuario ya está logueado

    form = UserCreationForm
    if request.method == "GET":
        return render(request, "signup.html", {"form": form})
    else:
        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    username=request.POST["username"],
                    password=request.POST["password1"],
                )
                user.save()
                login(request, user)
                return redirect("tasks")
            except:
                return render(
                    request,
                    "signup.html",
                    {"form": form, "error": "user already exists"},
                )
        # return HttpResponse("Don't match")
        return render(
            request, "signup.html", {"form": form, "error": "Password dont match"}
        )


def session(request):
    if request.user.is_authenticated:
        return redirect("tasks")  # Redirigir si el usuario ya está logueado

    if request.method == "GET":
        return render(request, "login.html", {"form": AuthenticationForm})
    else:
        print(request.POST)
        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"],
        )
        if user is None:
            return render(
                request,
                "login.html",
                {
                    "form": AuthenticationForm,
                    "error": "Username or Password is incorrect",
                },
            )
        else:
            login(request, user)
            return redirect("tasks")


def tasks(request):
    if request.user.is_authenticated:
        tasks = Task.objects.all()  # Devuelve todas las tareas
        # tasks = Task.objects.filter(user=request.user)  # Devuelve todas las tareas del usuario

        return render(
            request,
            "tasks.html",
            {"data": "aquí se verán las tasks creadas", "tasks": tasks},
        )
    return redirect("index")


def close_sesion(request):
    logout(request)
    return redirect("index")


def index(request):
    if request.user.is_authenticated:
        return redirect("tasks")  # Redirigir si el usuario ya está logueado
    return render(request, "index.html")


def profile(request):
    user = request.user
    profile = get_object_or_404(Profile, user=user)
    return render(request, "profile.html", {"profile": profile})


def edit_profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    return render(request, "profile.html", {"user": profile})


# def create_task(request):
#     if request.user.is_authenticated:
#         if request.method == "GET":
#             return render(request, "create_task.html", {"form": TaskForm})
#         else:

#             print(request.POST)  # ver datos
#             try:
#                 form = TaskForm(
#                     request.POST
#                 )  # Esto crea el html con los datos enviados
#                 nuevo_task = form.save(commit=False)  # Me devuelve los datos
#                 nuevo_task.user = request.user
#                 nuevo_task.save()
#                 print(nuevo_task)
#                 # Nota: Puedes hacerlo con el modelo tambien
#                 return redirect("tasks")
#             except:
#                 return render(
#                     request,
#                     "create_task.html",
#                     {"form": TaskForm, "error": "Error, ingresa los datos validos"},
#                 )
#     return redirect("index")


def create_task(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            return render(request, "create_task.html", {"form": TaskForm()})
        else:
            try:
                form = TaskForm(request.POST)
                if form.is_valid():
                    nuevo_task = form.save(commit=False)
                    nuevo_task.user = request.user
                    nuevo_task.save()
                    return redirect("tasks")
                else:
                    # Si el formulario no es válido, devuelve el formulario con errores
                    return render(
                        request,
                        "create_task.html",
                        {
                            "form": form,
                            "error": "Por favor, corrija los errores del formulario.",
                        },
                    )
            except Exception as e:
                # En caso de cualquier otro error
                return render(
                    request,
                    "create_task.html",
                    {"form": TaskForm(), "error": str(e)},
                )
    return redirect("index")


@login_required
def edit_profile(request):
    # Obtén el perfil del usuario actual
    profile = get_object_or_404(Profile, user=request.user)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            form.save()
            return redirect("profile")
        # Redirige a la página del perfil después de guardar
    else:
        form = ProfileForm(instance=profile)
        return render(request, "edit_profile.html", {"form": form})

    # <img src="{{ profile.avatar.url }}" alt="Avatar">
