from dependency_injector import providers
from rest_framework.permissions import IsAuthenticated
import inject


class ControllerInjectConfig:

    def inject_config(binder):
        permission_classes_provider = providers.Singleton(IsAuthenticated)
        binder.bind(IsAuthenticated, permission_classes_provider())

