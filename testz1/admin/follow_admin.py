from django.contrib import admin
from ..models import Follow

class FollowAdmin(admin.ModelAdmin):
    # Personaliza la visualización de los campos del modelo en el panel de administración
    list_display = ('follower', 'following', 'status')
    list_filter = ('follower', 'following', 'status')
    search_fields = ('follower', 'following', 'status')


# Registra el modelo User con la clase CustomUserAdmin
admin.site.register(Follow, FollowAdmin)