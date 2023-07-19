from graphene_django.utils.testing import GraphQLTestCase
from django.contrib.auth import get_user_model
from ..models import Notification, Follow, Idea
 
class NotificationTest(GraphQLTestCase):
    def test_notification_created_for_follower(self):

        # Crear dos usuarios para simular la relación de seguimiento
        follower = get_user_model().objects.create_user(email='follower@example.com', username='follower', password='testpassword')
        following = get_user_model().objects.create_user(email='following@example.com', username='following', password='testpassword')

        # Simular la relación de seguimiento entre los dos usuarios
        Follow.objects.create(follower=follower, following=following, status='approved')

        # Crear una nueva idea publicada por el usuario seguido (following)
        idea_text = 'Una nueva idea publicada por el usuario seguido'
        idea = Idea.objects.create(text=idea_text, author=following, visibility='public')

        # Verificar si se ha creado una notificación para el seguidor (follower)
        notifications = Notification.objects.filter(user=follower, idea=idea)
        self.assertEqual(notifications.count(), 1)