from graphene_django.utils.testing import GraphQLTestCase
from django.contrib.auth import get_user_model

class UserTest(GraphQLTestCase):

    GRAPHQL_URL = '/api/user/graphql/'

    def test_user_registration(self):
        """
        Prueba de registro de un nuevo usuario mediante el API GraphQL.
        """
        query = '''
            mutation {
                registerUser(email: "test@example.com", username: "testuser", password: "testpassword") {
                    user {
                        id
                        email
                        username
                    }
                }
            }
        '''
        response = self.query(query)
        self.assertResponseNoErrors(response)

        # Verificar que el usuario se haya registrado correctamente
        self.assertEqual(response.json()['data']['registerUser']['user']['email'], 'test@example.com')
        self.assertEqual(response.json()['data']['registerUser']['user']['username'], 'testuser')

    

    def test_user_login(self):
        """
        Prueba de inicio de sesión de usuario mediante el API GraphQL.
        """
        get_user_model().objects.create_user(email='test@example.com', username='testuser', password='testpassword')

        query = '''
            mutation {
                tokenAuth(email: "test@example.com", password: "testpassword") {
                    token
                }
            }
        '''
        response = self.query(query)
        self.assertResponseNoErrors(response)

        # Verificar que se haya recibido un token de autenticación
        self.assertIn('token', response.json()['data']['tokenAuth'])

    def test_change_password(self):
        """
        Prueba de cambio de contraseña de usuario mediante el API GraphQL.
        """
        get_user_model().objects.create_user(email='test@example.com', username='testuser', password='testpassword')

        # Autenticar el usuario antes de ejecutar la mutación
        self.client.login(email='test@example.com', password='testpassword')

        query = '''
            mutation {
                changePassword(email: "test@example.com", oldPassword: "testpassword", newPassword: "newpassword") {
                    user {
                        id
                        email
                    }
                }
            }
        '''

        response = self.query(query)
        self.assertResponseNoErrors(response)

        # Verificar que la contraseña se ha cambiado correctamente en la base de datos
        updated_user = get_user_model().objects.get(email='test@example.com')
        self.assertTrue(updated_user.check_password('newpassword'))
    
    def test_user_search(self):
        # Crear usuarios

        get_user_model().objects.create_user(email='user1@example.com', username='user1', password='testpassword')
        get_user_model().objects.create_user(email='user2@example.com', username='user2', password='testpassword')
        get_user_model().objects.create_user(email='other@example.com', username='other', password='testpassword')

        # Autenticar el usuario antes de ejecutar la mutación
        self.client.login(email='other@example.com', password='testpassword')

        # Realiza una búsqueda por parte del nombre de usuario
        query = '''
            query {
                searchUsers(searchQuery: "user") {
                    id
                    username
                    email
                }
            }
            '''
        
        response = self.query(query)

        # Verificar que no haya errores en la respuesta
        self.assertResponseNoErrors(response)

        self.assertEqual(len(response.json()['data']['searchUsers']), 2)
        usernames = {user['username'] for user in response.json()['data']['searchUsers']}
        self.assertSetEqual(usernames, {'user1', 'user2'})

        # Realiza una búsqueda por nombre de usuario completo
        query = '''
            query {
                searchUsers(searchQuery: "user1") {
                    id
                    username
                    email
                }
            }
            '''
        
        response = self.query(query)

        # Verificar que no haya errores en la respuesta
        self.assertResponseNoErrors(response)

        self.assertEqual(len(response.json()['data']['searchUsers']), 1)
        self.assertEqual(response.json()['data']['searchUsers'][0]['username'], 'user1')
