from django.urls import path, include


from herbie.views import SchemaRegistryView
from herbie.views import SaveBusinessEntityView
from herbie.views import DeleteBusinessEntityView


urlpatterns = [
    path('api/<str:business_entity>/save', SaveBusinessEntityView().as_view()),
    path('api/<str:business_entity>/delete', DeleteBusinessEntityView().as_view()),
    path('api/schema-registry/<str:business_entity>/<str:version>', SchemaRegistryView().as_view()),
    path('api/schema-registry/<str:business_entity>/', SchemaRegistryView().as_view(), {'version': ''}),
]
