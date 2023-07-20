from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        """Crea y guarda un nuevo usuario con el email, nombre de usuario y contraseña proporcionados."""
        if not email:
            raise ValueError('El email debe ser proporcionado')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        """Crea y guarda un nuevo superusuario con el email, nombre de usuario y contraseña proporcionados."""
        user = self.create_user(email, username, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    """Modelo personalizado de usuario que utiliza el email como nombre de usuario."""
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    email = models.EmailField(
        unique=True,
        verbose_name='Correo electrónico',
        help_text='Introduce tu dirección de correo electrónico.'
    )
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='Nombre de usuario',
        help_text='Introduce tu nombre de usuario.'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Activo',
        help_text='Indica si el usuario está activo.'
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name='Es personal',
        help_text='Indica si el usuario es parte del personal o staff.'
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
