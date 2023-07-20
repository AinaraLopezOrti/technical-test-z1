from django.db import models
from django.contrib.auth import get_user_model
from . import Idea

class Notification(models.Model):
    class Meta:
        verbose_name = 'Notificación'
        verbose_name_plural = 'Notificaciones'
        
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        verbose_name='Usuario',
        help_text='Selecciona el usuario al que se enviará esta notificación.'
    )
    idea = models.ForeignKey(
        Idea,
        on_delete=models.CASCADE,
        verbose_name='Idea relacionada',
        help_text='Selecciona la idea relacionada con esta notificación.'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de creación',
        help_text='Fecha y hora en que se creó esta notificación.'
    )
    mensaje = models.TextField(
        verbose_name='Mensaje',
        help_text='Escribe el contenido del mensaje de la notificación.'
    )
    leida = models.BooleanField(
        default=False,
        verbose_name='Leída',
        help_text='Indica si la notificación ha sido leída por el usuario.'
    )
    def __str__(self):
        return f"Notification for {self.user.username}: {self.idea.text}"
