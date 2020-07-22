from django.contrib.auth.models import AnonymousUser
from rest_framework.request import Request
from herbie_core.constants import ControllerConstants, GroupConstants
from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType

from herbie_core.models.models import AbstractBusinessEntity


class PermissionManager:
    def has_save_permission(self, business_entity: str, request: Request) -> bool:
        if type(request.user) == AnonymousUser:
            return False

        add_permission = self.get_permission_string(ControllerConstants.ADD, business_entity)
        change_permission = self.get_permission_string(ControllerConstants.CHANGE, business_entity)

        return (
            Permission.objects.filter(user=request.user)
            .filter(codename__in=[add_permission, change_permission])
            .count()
            == 2
        )

    def has_delete_permission(self, business_entity: str, request: Request) -> bool:
        delete_permission = self.get_permission_string(ControllerConstants.DELETE, business_entity)

        return Permission.objects.filter(user=request.user).filter(codename=delete_permission).exists()

    def get_view_permission(self, business_entity: str) -> Permission:
        view_permission = self.get_permission_string(ControllerConstants.VIEW, business_entity)

        return Permission.objects.get(codename=view_permission)

    def get_permission_string(self, action: str, business_entity: str) -> str:
        return action + "_" + self._remove_underscores(business_entity)

    def _remove_underscores(self, string: str) -> str:
        return string.replace("_", "")

    def create_group_and_permission_for_view_access(self):
        content_type = ContentType.objects.get_for_model(AbstractBusinessEntity)
        permission, created = Permission.objects.get_or_create(
            name="Can view all business entities", codename="view_business_entities", content_type=content_type,
        )

        group, created = Group.objects.get_or_create(name=GroupConstants.BUSINESS_ENTITIES_VIEW_GROUP)
        group.permissions.add(permission)
