from django.contrib import admin
from ..models import Idea

class IdeaAdmin(admin.ModelAdmin):
    # Personaliza la visualización de los campos del modelo en el panel de administración
    list_display = ('text', 'author', 'visibility', 'created_at')
    list_filter = ('author', 'visibility')
    search_fields = ('author', 'visibility')
    ordering = ('-created_at',)


# Registra el modelo User con la clase CustomUserAdmin
admin.site.register(Idea, IdeaAdmin)