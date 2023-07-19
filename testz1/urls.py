from graphene_django.views import GraphQLView
from django.urls import path

from .schemas.user_schema import schema


app_name = 'api'

urlpatterns = [
    path('graphql/', GraphQLView.as_view(graphiql=True, schema=schema)),
]