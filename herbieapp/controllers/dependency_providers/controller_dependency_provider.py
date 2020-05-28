from rest_framework.permissions import IsAuthenticated


class ControllerDependencyProvider:
    permission_classes_provider = IsAuthenticated()

