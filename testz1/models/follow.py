from django.db import models
from django.contrib.auth import get_user_model

# Definición de las opciones de estado para el modelo Follow
STATUS_CHOICES = (
    ('pending', 'Pendiente'),
    ('approved', 'Aprobado'),
    ('denied', 'Denegado'),
)

class Follow(models.Model):
    
    follower = models.ForeignKey(
        get_user_model(),
        related_name='follower',
        on_delete=models.CASCADE,
        verbose_name='Seguidor',
        help_text='Selecciona el usuario que está siguiendo a otro.'
    )
    following = models.ForeignKey(
        get_user_model(),
        related_name='following',
        on_delete=models.CASCADE,
        verbose_name='Siguiendo',
        help_text='Selecciona el usuario que está siendo seguido.'
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='Estado',
        help_text='Selecciona el estado de la relación de seguimiento.'
    )


    class Meta:
        unique_together = ('follower', 'following')
        verbose_name = 'Seguimiento'
        verbose_name_plural = 'Seguimientos'

    def __str__(self):
        return f'{self.follower} sigue a {self.following} (Estado: {self.status})'

