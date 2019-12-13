from django.contrib.auth.models import User


def process_roles(details, user, **kwargs):
    if User.objects.filter(username=user.get_username).exists() is False:
        user.is_staff = True
        user.is_superuser = True

        user.save()

