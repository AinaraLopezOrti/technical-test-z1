from django.db import models
from django.contrib.auth import get_user_model

# Definición de las opciones de estado para el modelo Follow
STATUS_CHOICES = (
    ('pending', 'Pendiente'),
    ('approved', 'Aprobado'),
    ('denied', 'Denegado'),
)

class Follow(models.Model):
    follower = models.ForeignKey(get_user_model(), related_name='follower', on_delete=models.CASCADE)
    following = models.ForeignKey(get_user_model(), related_name='following', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')


    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return f'{self.follower} sigue a {self.following} (Estado: {self.status})'

