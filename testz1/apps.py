from django.apps import AppConfig


class testz1Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'testz1'
    verbose_name = "Prueba técnica"

    def ready(self):
        from . import signals
