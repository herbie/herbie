from rest_framework.permissions import IsAuthenticated
from herbieapp.controllers.dependency_providers import ControllerDependencyProvider


class ControllerInjectConfig:
    def inject_config(binder):
        binder.bind(IsAuthenticated, ControllerDependencyProvider.permission_classes_provider)
