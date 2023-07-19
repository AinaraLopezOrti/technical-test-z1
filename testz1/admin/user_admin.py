from django.contrib import admin
from testz1.models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass
