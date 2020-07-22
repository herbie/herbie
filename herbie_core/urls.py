from django.urls import path

from herbie_core.views.delete_business_entity_view import DeleteBusinessEntityView
from herbie_core.views.save_business_entity_view import SaveBusinessEntityView
from herbie_core.views.schema_registry_view import SchemaRegistryView

urlpatterns = [
    path('<str:business_entity>/save', SaveBusinessEntityView().as_view()),
    path('<str:business_entity>/delete', DeleteBusinessEntityView().as_view()),
    path('schema-registry/<str:business_entity>/<str:version>', SchemaRegistryView().as_view()),
    path('schema-registry/<str:business_entity>/', SchemaRegistryView().as_view(), {'version': ''}),
]
