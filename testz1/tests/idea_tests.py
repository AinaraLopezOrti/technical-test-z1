from graphene_django.utils.testing import GraphQLTestCase
from django.contrib.auth import get_user_model
from ..models import Idea, Follow

class IdeaTest(GraphQLTestCase):
    GRAPHQL_URL = '/api/idea/graphql/'

    def test_create_idea(self):
        """
        Prueba de creación de una idea mediante el API GraphQL con usuario autenticado.
        """

        user = get_user_model().objects.create_user(email='test@example.com', username='testuser', password='testpassword')

        # Autenticar el usuario antes de ejecutar la mutación
        self.client.login(email='test@example.com', password='testpassword')
        
        query = '''
            mutation {
                createIdea(text: "Nueva idea", visibility: "private") {
                    idea {
                        id
                        text
                        author {
                            id
                            username
                        }
                    }
                }
            }
        '''
        response = self.query(query)

        # Verificar que no haya errores en la respuesta
        self.assertResponseNoErrors(response)

        # Verificar que la idea haya sido creada correctamente
        self.assertEqual(response.json()['data']['createIdea']['idea']['text'], 'Nueva idea')
        # Verificar que la idea esté relacionada con el usuario autenticado
        self.assertEqual(response.json()['data']['createIdea']['idea']['author']['username'], user.username)


    def test_change_visibility(self):
        """
        Prueba de modificación de la visibilidad de una idea de privado a protegido mediante el API GraphQL con usuario autenticado.
        """

        user = get_user_model().objects.create_user(email='test@example.com', username='testuser', password='testpassword')

        # Autenticar el usuario antes de ejecutar la mutación
        self.client.login(email='test@example.com', password='testpassword')
        
        query = '''
            mutation {
                createIdea(text: "Nueva idea", visibility: "private") {
                    idea {
                        id
                        text
                        visibility
                        author {
                            id
                            username
                        }
                    }
                }
            }
        '''
        response = self.query(query)

        # Verificar que no haya errores en la respuesta
        self.assertResponseNoErrors(response)

        # Verificar que la idea haya sido creada correctamente
        self.assertEqual(response.json()['data']['createIdea']['idea']['text'], 'Nueva idea')
        # Verificar que la idea esté relacionada con el usuario autenticado
        self.assertEqual(response.json()['data']['createIdea']['idea']['author']['username'], user.username)

        # Verificar que la idea tiene visibilidad privada
        self.assertEqual(response.json()['data']['createIdea']['idea']['visibility'], "PRIVATE")


        idea_id = response.json()['data']['createIdea']['idea']['id']
        query = '''
            mutation {
                setIdeaVisibility(visibility: "protected", ideaId: "%s") {
                    idea {
                        id
                        text
                        visibility
                        author {
                            id
                            username
                        }
                    }
                }
            }
        ''' % idea_id
        response = self.query(query)
        # Verificar que la idea tiene visibilidad privada
        self.assertEqual(response.json()['data']['setIdeaVisibility']['idea']['visibility'], "PROTECTED")


    def test_ideas_ordered_by_created_at(self):
        user = get_user_model().objects.create_user(email='test@example.com', username='testuser', password='testpassword')

        # Autenticar el usuario antes de ejecutar la mutación
        self.client.login(email='test@example.com', password='testpassword')

        Idea.objects.create(
            text='Idea 1',
            author=user,
            visibility='public',
        )
        Idea.objects.create(
            text='Idea 2',
            author=user,
            visibility='protected',
        )
        Idea.objects.create(
            text='Idea 3',
            author=user,
            visibility='private',
        )

        # Realiza una consulta GraphQL para obtener las ideas del usuario
        query = '''
            query {
                ideas {
                    id
                    text
                    visibility
                    createdAt
                }
            }
        '''

        # Usa la función `self.client.execute` para realizar la consulta GraphQL
        response = self.query(query)

        # Verifica que la consulta fue exitosa
        self.assertEqual(response.status_code, 200)

        # Obtén las ideas del resultado de la consulta
        ideas = response.json()['data']['ideas']

        # Verifica que las ideas estén ordenadas por fecha de creación (de más recientes a más antiguas)
        for i in range(len(ideas) - 1):
            self.assertGreaterEqual(ideas[i]['createdAt'], ideas[i + 1]['createdAt'])

    
    def test_delete_idea(self):
        user = get_user_model().objects.create_user(email='test@example.com', username='testuser', password='testpassword')

        idea = Idea.objects.create(
            text='Prueba de idea',
            author=user,
            visibility='public',
        )

        # Autenticar el usuario antes de ejecutar la mutación
        self.client.login(email='test@example.com', password='testpassword')


        # Realizar la mutación para eliminar la idea
        query = '''
            mutation {
              deleteIdea(ideaId: "%s") {
                success
              }
            }
        ''' % str(idea.id)

        response = self.query(query)
       # Verifica que la consulta fue exitosa
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['data']['deleteIdea']['success'])

        # Verificar que la idea se eliminó de la base de datos
        self.assertFalse(Idea.objects.filter(id=idea.id).exists())

    
    def test_get_ideas_by_user(self):
        user1 = get_user_model().objects.create_user(email='user1@example.com', username='user1', password='testpassword')
        get_user_model().objects.create_user(email='user2@example.com', username='user2', password='testpassword')
        user3 = get_user_model().objects.create_user(email='user3@example.com', username='user3', password='testpassword')

        # Crea algunas ideas de prueba para el usuario 1
        Idea.objects.create(text='Idea pública del usuario 1', author=user1, visibility='public')
        Idea.objects.create(text='Idea protegida del usuario 1', author=user1, visibility='protected')
        Idea.objects.create(text='Idea privada del usuario 1', author=user1, visibility='private')

        # Autenticar el usuario antes de ejecutar la mutación
        self.client.login(email='user3@example.com', password='testpassword')

        # Realiza una búsqueda de las ideas del usuario1 (autenticado como usuario3)
        query = '''
            query {
                ideasByUser(username: "user1") {
                    text
                    visibility
                }
            }
            '''
        
        response = self.query(query)

        # Verificar que no haya errores en la respuesta
        self.assertResponseNoErrors(response)

        # Verificar que la visibilidad es la correcta
        self.assertEqual(response.json()['data']['ideasByUser'][0]['visibility'], 'PUBLIC')

        Follow.objects.create(follower=user1, following=user3, status='approved')
        Follow.objects.create(follower=user3, following=user1, status='approved')

        # Realiza una búsqueda de las ideas del usuario1 (autenticado como usuario3) siguiendose mutuamente
        query = '''
            query {
                ideasByUser(username: "user1") {
                    text
                    visibility
                }
            }
            '''
        
        response = self.query(query)

        # Verificar que no haya errores en la respuesta
        self.assertResponseNoErrors(response)

        self.assertEqual(len(response.json()['data']['ideasByUser']), 2)
        visibilities = {idea['visibility'] for idea in response.json()['data']['ideasByUser']}
        self.assertSetEqual(visibilities, {'PUBLIC', 'PROTECTED'})

    def test_timeline(self):
        # Crea algunos usuarios de prueba
        user1 = get_user_model().objects.create_user(email='user1@example.com', username='user1', password='testpassword')
        user2 = get_user_model().objects.create_user(email='user2@example.com', username='user2', password='testpassword')

        # Crea algunas ideas de prueba para el usuario 1
        Idea.objects.create(text='Idea pública del usuario 1', author=user1, visibility='public')
        Idea.objects.create(text='Idea protegida del usuario 1', author=user1, visibility='protected')

        # Crea algunas ideas de prueba para el usuario 2
        Idea.objects.create(text='Idea pública del usuario 2', author=user2, visibility='public')
        Idea.objects.create(text='Idea privada del usuario 2', author=user2, visibility='private')

        # Crea una relación de seguimiento entre los usuarios
        Follow.objects.create(follower=user1, following=user2, status='approved')

        # Autenticar el usuario antes de ejecutar la mutación
        self.client.login(email='user1@example.com', password='testpassword')

        # Realiza una búsqueda del timeline del usuario1 (autenticado como usuario1)
        query = '''
            query {
                timeline {
                    text
                    visibility
                    createdAt
                    author {
                        username
                    }
                }
            }
            '''
        
        response = self.query(query)

        # Verificar que no haya errores en la respuesta
        self.assertResponseNoErrors(response)

        self.assertEqual(len(response.json()['data']['timeline']), 3)

        # Verificar que las ideas estén ordenadas por fecha de creación
        timeline_ideas = response.json()['data']['timeline']
        for i in range(len(timeline_ideas) - 1):
            self.assertGreaterEqual(timeline_ideas[i]['createdAt'], timeline_ideas[i + 1]['createdAt'])
        

        # Autenticar el usuario antes de ejecutar la mutación
        self.client.login(email='user2@example.com', password='testpassword')
        # Realiza una búsqueda del timeline del usuario2 (autenticado como usuario2)
        query = '''
            query {
                timeline {
                    text
                    visibility
                    createdAt
                    author {
                        username
                    }
                }
            }
            '''

        response = self.query(query)

        # Verificar que no haya errores en la respuesta
        self.assertResponseNoErrors(response)

        self.assertEqual(len(response.json()['data']['timeline']), 2)

        # Verificar que las ideas estén ordenadas por fecha de creación
        timeline_ideas = response.json()['data']['timeline']
        for i in range(len(timeline_ideas) - 1):
            self.assertGreaterEqual(timeline_ideas[i]['createdAt'], timeline_ideas[i + 1]['createdAt'])
        




