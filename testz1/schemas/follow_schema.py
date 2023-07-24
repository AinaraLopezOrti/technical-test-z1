import graphene
from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import login_required
from django.contrib.auth import get_user_model
from ..models import Follow, STATUS_CHOICES
from .user_schema import UserType

class FollowRequestType(DjangoObjectType):
    class Meta:
        model = Follow

class FollowRequestMutation(graphene.Mutation):
    class Arguments:
        user_id = graphene.ID(required=True)

    success = graphene.Boolean()
    follow_id = graphene.ID()

    @login_required
    def mutate(self, info, user_id):
        user = info.context.user
        if not user.is_authenticated:
            raise Exception("You must be logged in to perform this action.")

        try:
            following_user = get_user_model().objects.get(pk=user_id)
        except get_user_model().DoesNotExist:
            raise Exception("User does not exist.")
        
        if following_user == user:
            raise Exception("You cannot follow yourself.")

        follow_request = Follow.objects.create(follower=user, following=following_user, status='pending')

        return FollowRequestMutation(success=True, follow_id=str(follow_request.id))
    
class RespondToFollowRequest(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        follow_id = graphene.ID(required=True)
        status = graphene.String(required=True)

    @login_required
    def mutate(self, info, follow_id, status):
        # Verificar si la solicitud de seguimiento existe y si el usuario autenticado es el destinatario
        try:
            follow_request = Follow.objects.get(id=follow_id, following=info.context.user, status='pending')
        except Follow.DoesNotExist:
            raise Exception('La solicitud de seguimiento no existe o ya ha sido respondida.')

        # Verificar si el estado proporcionado es válido
        valid_status_choices = [choice[0] for choice in STATUS_CHOICES]
        if status not in valid_status_choices:
            raise Exception('El estado proporcionado no es válido.')

        # Actualizar el estado de la solicitud de seguimiento y guardarla en la base de datos
        follow_request.status = status
        follow_request.save()

        return RespondToFollowRequest(success=True)


class UnfollowUser(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        user_id = graphene.ID(required=True)

    @login_required
    def mutate(self, info, user_id):
        # Verificar si la relación de seguimiento existe y si el usuario autenticado es el seguidor
        try:
            follow_relationship = Follow.objects.get(follower=info.context.user, following_id=user_id, status='approved')
        except Follow.DoesNotExist:
            raise Exception('No estás siguiendo a este usuario.')

        # Eliminar la relación de seguimiento de la base de datos
        follow_relationship.delete()

        return UnfollowUser(success=True)


class RemoveFollower(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        follower_id = graphene.ID(required=True)

    @login_required
    def mutate(self, info, follower_id):
        # Verificar si la relación de seguimiento existe y si el usuario autenticado es el seguido
        try:
            follow_relationship = Follow.objects.get(follower_id=follower_id, following=info.context.user, status='approved')
        except Follow.DoesNotExist:
            raise Exception('No existe una relación de seguimiento con este usuario.')

        # Eliminar la relación de seguimiento de la base de datos
        follow_relationship.delete()

        return RemoveFollower(success=True)

class Mutation(graphene.ObjectType):
    """Definición de las mutaciones disponibles."""
    respond_to_follow_request = RespondToFollowRequest.Field()
    request_follow = FollowRequestMutation.Field()
    unfollow_user = UnfollowUser.Field()
    remove_follower = RemoveFollower.Field()

 
class Query(graphene.ObjectType):
    """Definición de las consultas disponibles."""
    follow_requests_received = graphene.List(FollowRequestType)
    following = graphene.List(UserType)
    followers = graphene.List(UserType)

    @login_required
    def resolve_follow_requests_received(self, info):
        # Obtener las solicitudes de seguimiento recibidas por el usuario autenticado
        user = info.context.user
        return Follow.objects.filter(following=user, status='pending')
    
    @login_required
    def resolve_following(self, info):
        # Obtener la lista de usuarios que sigue el usuario autenticado
        user = info.context.user
        following_users = Follow.objects.filter(follower=user, status='approved')
        return [follow.following for follow in following_users]

    @login_required
    def resolve_followers(self, info):
        # Obtener la lista de usuarios que siguen al usuario autenticado
        user = info.context.user
        follower_users = Follow.objects.filter(following=user, status='approved')
        return [follow.follower for follow in follower_users]

schema = graphene.Schema(query=Query, mutation=Mutation)