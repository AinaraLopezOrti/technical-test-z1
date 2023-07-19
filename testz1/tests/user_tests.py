from graphene_django.utils.testing import GraphQLTestCase
from django.contrib.auth import get_user_model
from graphql_jwt.shortcuts import get_token
from graphql_jwt.testcases import JSONWebTokenTestCase

class UserRegistrationTest(GraphQLTestCase):
    GRAPHQL_URL = '/api/graphql/'

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
        user = get_user_model().objects.create_user(email='test@example.com', username='testuser', password='testpassword')

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
        user = get_user_model().objects.create_user(email='test@example.com', username='testuser', password='testpassword')

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
