from rest_framework.permissions import IsAuthenticated
#from dependency_injector import containers, providers


class ControllerDependencyProvider: #(containers.DeclarativeContainer):
    permission_classes_provider = IsAuthenticated()

    # Using dependency injector package
    # permission_classes_provider = providers.Singleton(IsAuthenticated)


