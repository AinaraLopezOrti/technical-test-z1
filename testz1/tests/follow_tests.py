from graphene_django.utils.testing import GraphQLTestCase
from django.contrib.auth import get_user_model
from ..models import Follow

class FollowTest(GraphQLTestCase):
    GRAPHQL_URL = '/api/follow/graphql/'

    def test_follow_request(self):
        # Crea una solicitud de seguimiento de un usuario de prueba a otro
        follower = get_user_model().objects.create_user(email='follower@example.com', username='follower', password='testpassword')
        following = get_user_model().objects.create_user(email='following@example.com', username='following', password='testpassword')

        # Autenticar el usuario que realizará la solicitud
        self.client.login(email='follower@example.com', password='testpassword')

        # Ejecuta la mutación para solicitar seguir al usuario
        query = '''
            mutation {
                requestFollow(userId: "%s") {
                    success
                    followId
                }
            }
        ''' % following.id

        response = self.query(query)

        # Verificar que no haya errores en la respuesta
        self.assertResponseNoErrors(response)

        # Verifica que la mutación fue exitosa
        self.assertTrue(response.json()['data']['requestFollow']['success'])

        # Verificar que la solicitud de seguimiento fue creada en la base de datos y tiene estado "pending"
        follow_request = Follow.objects.filter(follower=follower, following=following, status='pending').first()
        self.assertIsNotNone(follow_request)


    def test_respond_to_follow_request(self):
        # Crea una solicitud de seguimiento de un usuario de prueba a otro
        follower = get_user_model().objects.create_user(email='follower@example.com', username='follower', password='testpassword')
        following = get_user_model().objects.create_user(email='following@example.com', username='following', password='testpassword')
        follow_request = Follow.objects.create(follower=follower, following=following)

        # Autenticar el usuario antes de ejecutar la mutación
        self.client.login(email='following@example.com', password='testpassword')

        # Ejecuta la mutación para aprobar la solicitud de seguimiento
        query ='''
            mutation {
                respondToFollowRequest(followId: "%s", status: "approved") {
                    success
                }
            }
        ''' % follow_request.id

        response = self.query(query)

        # Verificar que no haya errores en la respuesta
        self.assertResponseNoErrors(response)

        # Verificar que el estado se ha modificado
        self.assertTrue(response.json()['data']['respondToFollowRequest']['success'])
        follow_request.refresh_from_db()
        self.assertEqual(follow_request.status,'approved')
    

    def test_follow_requests_received(self):
        # Crea una solicitud de seguimiento recibida para el usuario de prueba
        follower = get_user_model().objects.create_user(email='follower@example.com', username='follower', password='testpassword')
        following = get_user_model().objects.create_user(email='following@example.com', username='following', password='testpassword')
        follow_request = Follow.objects.create(follower=follower, following=following, status='pending')

        # Autenticar el usuario antes de ejecutar la mutación
        self.client.login(email='following@example.com', password='testpassword')

        # Ejecuta la consulta para obtener las solicitudes de seguimiento recibidas
        query = '''
            query {
                followRequestsReceived {
                    id
                    follower {
                        id
                        username
                    }
                }
            }
        '''

        response = self.query(query)

        # Verificar que no haya errores en la respuesta
        self.assertResponseNoErrors(response)

        # Verifica que la solicitud de seguimiento recibida está en la respuesta
        self.assertEqual(response.json()['data']['followRequestsReceived'][0]['id'], str(follow_request.id))
        self.assertEqual(response.json()['data']['followRequestsReceived'][0]['follower']['id'], str(follower.id))
        self.assertEqual(response.json()['data']['followRequestsReceived'][0]['follower']['username'], follower.username)
    

    def test_following(self):
        # Crea una relación de seguimiento entre el usuario de prueba y otro usuario
        follower = get_user_model().objects.create_user(email='follower@example.com', username='follower', password='testpassword')
        following = get_user_model().objects.create_user(email='following@example.com', username='following', password='testpassword')
        Follow.objects.create(follower=follower, following=following, status='approved')

        # Autenticar el usuario antes de ejecutar la mutación
        self.client.login(email='follower@example.com', password='testpassword')

        # Ejecuta la consulta para obtener la lista de usuarios seguidos por el usuario de prueba
        query = '''
            query {
                following {
                    id
                    username
                }
            }
        '''

        response = self.query(query)

        # Verificar que no haya errores en la respuesta
        self.assertResponseNoErrors(response)

        # Verifica que el usuario seguido está en la respuesta
        self.assertEqual(len(response.json()['data']['following']), 1)
        self.assertEqual(response.json()['data']['following'][0]['id'], str(following.id))
        self.assertEqual(response.json()['data']['following'][0]['username'], following.username)


    def test_followers(self):
        # Crea una relación de seguimiento entre otro usuario y el usuario de prueba
        follower = get_user_model().objects.create_user(email='follower@example.com', username='follower', password='testpassword')
        following = get_user_model().objects.create_user(email='following@example.com', username='following', password='testpassword')
        Follow.objects.create(follower=follower, following=following, status='approved')

        # Autenticar el usuario antes de ejecutar la mutación
        self.client.login(email='following@example.com', password='testpassword')

        # Ejecuta la consulta para obtener la lista de usuarios que siguen al usuario de prueba
        query = '''
            query {
                followers {
                    id
                    username
                }
            }
        '''

        response = self.query(query)

        # Verificar que no haya errores en la respuesta
        self.assertResponseNoErrors(response)

        # Verifica que el usuario seguido está en la respuesta
        self.assertEqual(len(response.json()['data']['followers']), 1)
        self.assertEqual(response.json()['data']['followers'][0]['id'], str(follower.id))
        self.assertEqual(response.json()['data']['followers'][0]['username'], follower.username)
    

    def test_unfollow_user(self):
        # Crea una relación de seguimiento entre el usuario de prueba y otro usuario
        follower = get_user_model().objects.create_user(email='follower@example.com', username='follower', password='testpassword')
        following = get_user_model().objects.create_user(email='following@example.com', username='following', password='testpassword')
        Follow.objects.create(follower=follower, following=following, status='approved')

        # Autenticar el usuario antes de ejecutar la mutación
        self.client.login(email='follower@example.com', password='testpassword')


        # Ejecuta la mutación para dejar de seguir al usuario
        query = '''
            mutation {
                unfollowUser(userId: "%s") {
                    success
                }
            }
        ''' % following.id

        response = self.query(query)

        # Verificar que no haya errores en la respuesta
        self.assertResponseNoErrors(response)

        # Verifica que la mutación fue exitosa
        self.assertTrue(response.json()['data']['unfollowUser']['success'])

        # Verifica que la relación de seguimiento haya sido eliminada de la base de datos
        self.assertFalse(Follow.objects.filter(follower=follower, following=following, status='approved').exists())
    

    def test_remove_follower(self):
        # Crea una relación de seguimiento entre el usuario de prueba y otro usuario
        follower = get_user_model().objects.create_user(email='follower@example.com', username='follower', password='testpassword')
        following = get_user_model().objects.create_user(email='following@example.com', username='following', password='testpassword')
        Follow.objects.create(follower=follower, following=following, status='approved')

        # Autenticar el usuario antes de ejecutar la mutación
        self.client.login(email='following@example.com', password='testpassword')


        # Ejecuta la mutación para eliminar al seguidor
        query = '''
            mutation {
                removeFollower(followerId: "%s") {
                    success
                }
            }
        ''' % follower.id

        response = self.query(query)

        # Verificar que no haya errores en la respuesta
        self.assertResponseNoErrors(response)

        # Verifica que la mutación fue exitosa
        self.assertTrue(response.json()['data']['removeFollower']['success'])

        # Verifica que la relación de seguimiento haya sido eliminada de la base de datos
        self.assertFalse(Follow.objects.filter(follower=follower, following=following).exists())
