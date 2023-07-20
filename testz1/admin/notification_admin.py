from django.contrib import admin
from ..models import Notification

class NotificationAdmin(admin.ModelAdmin):
    # Personaliza la visualización de los campos del modelo en el panel de administración
    list_display = ('user', 'idea', 'created_at')
    list_filter = ('user', 'idea')
    search_fields = ('user', 'idea')
    ordering = ('-created_at',)


# Registra el modelo User con la clase CustomUserAdmin
admin.site.register(Notification, NotificationAdmin)