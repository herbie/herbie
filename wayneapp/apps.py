from django.apps import AppConfig
from django.db.models.signals import post_migrate
from wayne import settings


class WayneappConfig(AppConfig):
    name = settings.APP_LABEL

    def ready(self):
        from wayneapp.services.permission_manager import PermissionManager
        post_migrate.connect(PermissionManager.create_group_and_permission_for_view_access, sender=self)
