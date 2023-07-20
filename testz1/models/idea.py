# Modelo para las ideas
from django.db import models
from . import User

VISIBILITY_CHOICES = (
    ('public', 'Pública'),
    ('protected', 'Protegida'),
    ('private', 'Privada'),
)

class Idea(models.Model):
    class Meta:
        verbose_name = 'Idea'
        verbose_name_plural = 'Ideas'

    text = models.CharField(max_length=200, 
                            verbose_name='Texto',
                            help_text='Escribe el contenido de la idea (máximo 200 caracteres).')
    
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE, 
                               verbose_name='Autor',
                               help_text='Selecciona el autor de la idea.')
    
    visibility = models.CharField(max_length=20, 
                                  choices=VISIBILITY_CHOICES, 
                                  default='public', 
                                  verbose_name='Visibilidad',
                                  help_text='Selecciona la visibilidad de la idea.')
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de creación',
        help_text='Fecha de creación'
    )

    def __str__(self):
        return self.text