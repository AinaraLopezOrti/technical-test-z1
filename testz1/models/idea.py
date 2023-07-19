# Modelo para las ideas
from django.db import models
from . import User

VISIBILITY_CHOICES = (
    ('public', 'Pública'),
    ('protected', 'Protegida'),
    ('private', 'Privada'),
)

class Idea(models.Model):
    text = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    visibility = models.CharField(max_length=20, choices=VISIBILITY_CHOICES, default='public')
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de creación',
        help_text='Fecha de creación'
    )

    def __str__(self):
        return self.text