from django.urls import path

from herbie_core.views import SchemaRegistryView
from herbie_core.views import SaveBusinessEntityView
from herbie_core.views import DeleteBusinessEntityView


urlpatterns = [
    path('api/<str:business_entity>/save', SaveBusinessEntityView().as_view()),
    path('api/<str:business_entity>/delete', DeleteBusinessEntityView().as_view()),
    path('api/schema-registry/<str:business_entity>/<str:version>', SchemaRegistryView().as_view()),
    path('api/schema-registry/<str:business_entity>/', SchemaRegistryView().as_view(), {'version': ''}),
]
