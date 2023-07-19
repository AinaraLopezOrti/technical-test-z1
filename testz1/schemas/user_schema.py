import graphene
from graphene_django.types import DjangoObjectType
from django.contrib.auth import get_user_model
# from django.core.mail import send_mail
from graphql_jwt.decorators import login_required
from graphql_jwt import ObtainJSONWebToken
import graphql_jwt
from django.contrib.auth.tokens import default_token_generator
from ..models import Idea, VISIBILITY_CHOICES
from rest_framework.authtoken.models import Token

class UserType(DjangoObjectType):
    """Definición del tipo GraphQL para el modelo de usuario."""
    class Meta:
        model = get_user_model()

# Definición del tipo GraphQL para el modelo de Idea
class IdeaType(DjangoObjectType):
    class Meta:
        model = Idea

class RegisterUser(graphene.Mutation):
    """Mutación para registrar un nuevo usuario."""
    user = graphene.Field(UserType)

    class Arguments:
        email = graphene.String(required=True)
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, email, username, password):
        user = get_user_model().objects.create_user(
            email=email,
            username=username,
            password=password,
        )

        return RegisterUser(user=user)


class ChangePassword(graphene.Mutation):
    """Mutación para cambiar la contraseña de un usuario."""
    user = graphene.Field(UserType)

    class Arguments:
        email = graphene.String(required=True)
        old_password = graphene.String(required=True)
        new_password = graphene.String(required=True)

    @login_required
    def mutate(self, info, email, old_password, new_password):
        user = get_user_model().objects.get(email=email)
        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return ChangePassword(user=user)
        raise Exception('Contraseña incorrecta.')

class ObtainJSONWebToken(ObtainJSONWebToken):
    user = graphene.Field(UserType)

    @classmethod
    def resolve(cls, root, info, **kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Usuario no autenticado.')
        return cls(user=user)


class ResetPassword(graphene.Mutation):
    """
    Mutación para restablecer la contraseña de un usuario y enviar un email con un enlace mágico.
    """
    success = graphene.Boolean()

    class Arguments:
        email = graphene.String(required=True)

    @classmethod
    def mutate(cls, root, info, email):
        user = get_user_model().objects.get(email=email)
        if user:
            # Generar un token para restablecer la contraseña
            token = default_token_generator.make_token(user)

            # Crear un enlace mágico con el token y enviarlo por correo electrónico
            reset_link = f'http://example.com/reset-password?email={email}&token={token}'

            # Simulador de envio de correo electronico
            # send_mail(
            #     'Restablecer contraseña',
            #     f'Haga clic en el siguiente enlace para restablecer su contraseña: {reset_link}',
            #     'your-email@example.com', 
            #     [email],
            #     fail_silently=False,
            # )
            return cls(success=True)
        return cls(success=False)

class CreateIdea(graphene.Mutation):
    idea = graphene.Field(IdeaType)

    class Arguments:
        text = graphene.String(required=True)
        visibility = graphene.String(required=True)

    @login_required
    def mutate(self, info, text, visibility):
        # Obtener el usuario autenticado utilizando la variable "info" proporcionada por GraphQL
        user = info.context.user

        # Crear la nueva idea y asociarla al autor (usuario autenticado)
        valid_visibility_choices = [choice[0] for choice in VISIBILITY_CHOICES]
        if visibility not in valid_visibility_choices:
            raise Exception('La visibilidad seleccionada no es válida.')

        # Actualizar la visibilidad de la idea y guardarla en la base de datos
        idea.visibility = visibility
        idea = Idea.objects.create(text=text, author=user, visibility=visibility)

        # Devolver la idea creada en la respuesta
        return CreateIdea(idea=idea)


class SetIdeaVisibility(graphene.Mutation):
    idea = graphene.Field(IdeaType)

    class Arguments:
        idea_id = graphene.ID(required=True)
        visibility = graphene.String(required=True)
        token = graphene.String(required=True)  # Agregar argumento para el token

    def mutate(self, info, idea_id, visibility, token):  # Agregar argumento 'token' a la función
        # Verificar el token y obtener el usuario autenticado
        try:
            user = Token.objects.get(key=token).user
        except Token.DoesNotExist:
            raise Exception('Token de autenticación inválido.')

        # Verificar si el usuario es el autor de la idea
        try:
            idea = Idea.objects.get(id=idea_id)
        except Idea.DoesNotExist:
            raise Exception('La idea no existe.')

        if user != idea.author:
            raise Exception('No tienes permisos para cambiar la visibilidad de esta idea.')

        # Verificar si la visibilidad es una opción válida
        valid_visibility_choices = [choice[0] for choice in VISIBILITY_CHOICES]
        if visibility not in valid_visibility_choices:
            raise Exception('La visibilidad seleccionada no es válida.')

        # Actualizar la visibilidad de la idea y guardarla en la base de datos
        idea.visibility = visibility
        idea.save()

        return SetIdeaVisibility(idea=idea)

    
class Mutation(graphene.ObjectType):
    """Definición de las mutaciones disponibles."""
    register_user = RegisterUser.Field()
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    change_password = ChangePassword.Field()
    token_auth = ObtainJSONWebToken.Field()
    reset_password = ResetPassword.Field()
    create_idea = CreateIdea.Field()
    set_idea_visibility = SetIdeaVisibility.Field()

class Query(graphene.ObjectType):
    """Definición de las consultas disponibles."""
    users = graphene.List(UserType)
    logged_in = graphene.List(UserType)
    ideas = graphene.List(IdeaType)

    def resolve_users(self, info):
        """Consulta para obtener todos los usuarios registrados."""
        return get_user_model().objects.all()
    
    @login_required
    def resolve_logged_in(self, info):
        return info.context.user
    
    @login_required
    def resolve_ideas(self, info):
        # Consultar todas las ideas
        return Idea.objects.all()

schema = graphene.Schema(query=Query, mutation=Mutation)