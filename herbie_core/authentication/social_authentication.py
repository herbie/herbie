from django.contrib.auth.models import User, Group
from herbie_core.constants import GroupConstants


def process_roles(details, user, **kwargs):
    if not User.objects.filter(username=user.get_username).exists():
        my_group = Group.objects.get(name=GroupConstants.BUSINESS_ENTITIES_VIEW_GROUP)
        user.is_staff = True
        user.groups.add(my_group)
        user.save()
