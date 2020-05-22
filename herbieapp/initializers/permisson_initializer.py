from herbieapp.initializers.abstract_initializer import AbstractInitializer
from herbieapp.services.permission_manager import PermissionManager


class PermissionInitializer(AbstractInitializer):
    _permission_manager = None

    def __init__(
            self,
            permission_manager: PermissionManager,
            **kwargs
    ):
        self._permission_manager = permission_manager

    def get_name(self) -> str:
        return 'permissions'

    def init(self):
        self._permission_manager.create_group_and_permission_for_view_access()
