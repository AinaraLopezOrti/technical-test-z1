from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Follow, Idea, Notification

@receiver(post_save, sender=Idea)
def create_notification(sender, instance, created, **kwargs):
    if created:
        # Obtener los usuarios que siguen al autor de la idea
        followers = Follow.objects.filter(following=instance.author, status='approved')

        # Crear una notificación para cada seguidor que tenga acceso a la idea
        for follower in followers:
            if instance.visibility == 'public' or (instance.visibility == 'protected' and follower.follower == instance.author):
                Notification.objects.create(user=follower.follower, idea=instance)
