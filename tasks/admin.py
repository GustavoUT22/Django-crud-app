from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Task, Profile
from django.contrib.auth.models import User


# Inline admin para el modelo Profile
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = "Profile"


# Extender el UserAdmin original para incluir el ProfileInline
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)


class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ("created",)


# Register your models here.
admin.site.register(Task, TaskAdmin)
