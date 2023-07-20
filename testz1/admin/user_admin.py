from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from ..models import User

class CustomUserAdmin(UserAdmin):
    # Personaliza la visualización de los campos del modelo en el panel de administración
    list_display = ('email', 'username', 'is_active', 'is_staff')
    list_filter = ('is_active', 'is_staff')
    search_fields = ('email', 'username')
    ordering = ('email',)

# Registra el modelo User con la clase CustomUserAdmin
admin.site.register(User, CustomUserAdmin)