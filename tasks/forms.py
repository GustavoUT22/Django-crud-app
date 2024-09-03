from django.forms import ModelForm
from .models import Profile
from .models import Task


class TaskForm(ModelForm):
    class Meta:
        # Definir en que modelo se basa el formulario, en este caso Task
        model = Task
        # Defines los campos  que quieres poder rellenar a traves del formulario
        fields = ["title", "description", "important"]  # Solo los necesarios


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ["biography", "avatar"]
