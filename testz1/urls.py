from graphene_django.views import GraphQLView
from django.urls import path

from .schemas.user_schema import schema as UserSchema
from .schemas.idea_schema import schema as IdeaSchema
from .schemas.follow_schema import schema as FollowSchema

app_name = 'api'

urlpatterns = [
    path('user/graphql/', GraphQLView.as_view(graphiql=True, schema=UserSchema)),
    path('idea/graphql/', GraphQLView.as_view(graphiql=True, schema=IdeaSchema)),
    path('follow/graphql/', GraphQLView.as_view(graphiql=True, schema=FollowSchema)),
]