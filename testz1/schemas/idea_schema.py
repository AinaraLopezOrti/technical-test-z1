import graphene
from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import F
from ..models import Idea, VISIBILITY_CHOICES, Follow

# Definición del tipo GraphQL para el modelo de Idea
class IdeaType(DjangoObjectType):
    class Meta:
        model = Idea


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

        idea = Idea.objects.create(text=text, author=user, visibility=visibility)

        # Devolver la idea creada en la respuesta
        return CreateIdea(idea=idea)


class SetIdeaVisibility(graphene.Mutation):
    idea = graphene.Field(IdeaType)

    class Arguments:
        idea_id = graphene.ID(required=True)
        visibility = graphene.String(required=True)

    @login_required
    def mutate(self, info, idea_id, visibility):

        # Verificar si el usuario es el autor de la idea
        try:
            idea = Idea.objects.get(id=idea_id)
        except Idea.DoesNotExist:
            raise Exception('La idea no existe.')

        if info.context.user != idea.author:
            raise Exception('No tienes permisos para cambiar la visibilidad de esta idea.')

        # Verificar si la visibilidad es una opción válida
        valid_visibility_choices = [choice[0] for choice in VISIBILITY_CHOICES]
        if visibility not in valid_visibility_choices:
            raise Exception('La visibilidad seleccionada no es válida.')

        # Actualizar la visibilidad de la idea y guardarla en la base de datos
        idea.visibility = visibility
        idea.save()

        return SetIdeaVisibility(idea=idea)

class DeleteIdea(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        idea_id = graphene.ID(required=True)

    @login_required
    def mutate(self, info, idea_id):
        # Verificar si la idea existe y si el usuario autenticado es el autor
        try:
            idea = Idea.objects.get(id=idea_id)
        except Idea.DoesNotExist:
            raise Exception('La idea no existe.')

        if info.context.user != idea.author:
            raise Exception('No tienes permisos para eliminar esta idea.')

        # Eliminar la idea de la base de datos
        idea.delete()

        return DeleteIdea(success=True)



class Mutation(graphene.ObjectType):
    """Definición de las mutaciones disponibles."""
    create_idea = CreateIdea.Field()
    set_idea_visibility = SetIdeaVisibility.Field()
    delete_idea = DeleteIdea.Field()
    

class Query(graphene.ObjectType):
    """Definición de las consultas disponibles."""
    ideas = graphene.List(IdeaType)
    ideas_by_user = graphene.List(IdeaType, username=graphene.String(required=True))
    timeline = graphene.List(IdeaType)
    
    @login_required
    def resolve_ideas(self, info):
        # Consultar todas las ideas del usuario autenticado ordenadas de mas recientes a mas antiguas
        user = info.context.user
        return Idea.objects.filter(author=user).order_by(F('created_at').desc())
    
    @login_required
    def resolve_ideas_by_user(self, info, username):
        # Obtener el usuario cuyas ideas queremos ver
        try:
            user = get_user_model().objects.get(username=username)
        except get_user_model().DoesNotExist:
            raise Exception('El usuario especificado no existe.')

        # Obtener todas las ideas del usuario
        ideas = Idea.objects.filter(author=user)

        following_users = []

        # Obtén la lista de usuarios que sigue
        following_users = Follow.objects.filter(follower=info.context.user, status='approved').values_list('following', flat=True)

        visible_ideas = []

        for idea in ideas:
            if idea.visibility == 'public':
                # Idea pública, siempre visible para todos
                visible_ideas.append(idea)
            elif idea.visibility == 'protected' and (idea.author.id in following_users or idea.author == info.context.user):
                # Idea protegida, solo visible si el autor es seguido por el usuario autenticado
                visible_ideas.append(idea)
            elif idea.visibility == 'private' and idea.author == info.context.user:
                # Idea privada, solo visible para el propio usuario
                visible_ideas.append(idea)

        return visible_ideas

    @login_required
    def resolve_timeline(self, info):
        # Obtener el usuario autenticado desde el contexto
        user = info.context.user

        # Obtener todas las ideas del usuario autenticado
        user_ideas = Idea.objects.filter(author=user)

        # Obtener la lista de usuarios que sigue el usuario autenticado
        following_users = Follow.objects.filter(follower=user, status='approved').values_list('following', flat=True)

        # Obtener todas las ideas de los usuarios seguidos por el usuario autenticado con visibilidad "public" o "protected"
        following_ideas = Idea.objects.filter(author__in=following_users, visibility__in=['public', 'protected'])

        # Combinar y ordenar las ideas en un solo timeline
        timeline_ideas = list(user_ideas) + list(following_ideas)
        timeline_ideas.sort(key=lambda idea: idea.created_at, reverse=True)

        return timeline_ideas

schema = graphene.Schema(query=Query, mutation=Mutation)