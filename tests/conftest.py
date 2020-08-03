import fnmatch
import os
import environ
import pytest

from django.core.management import call_command
from django.conf import settings

env = environ.Env()


def pytest_configure(config):
    settings.configure(
        APP_LABEL="herbie_core",
        SECRET_KEY="not very secret in tests",
        SCHEMA_REGISTRY_PACKAGE="test",
        MESSAGING_PROVIDER="google_pubsub",
        LANGUAGE_CODE="en-us",
        TIME_ZONE="UTC",
        USE_I18N=True,
        USE_L10N=True,
        USE_TZ=True,
        STATIC_URL="/static/",
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.postgresql_psycopg2",
                "NAME": "herbie_test_db",
                "USER": "user",
                "PASSWORD": "password",
                "HOST": env.str("DB_HOST", "localhost"),
                "PORT": env.str("DB_PORT", "5432"),
            }
        },
        JSON_VIEWER={"JS_URL": "json-viewer/jquery.json-viewer.js", "CSS_URL": "json-viewer/jquery.json-viewer.css"},
        INSTALLED_APPS=(
            "django.contrib.admin",
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sessions",
            "django.contrib.messages",
            "django.contrib.staticfiles",
            "rest_framework",
            "rest_framework.authtoken",
            "herbie_core",
        ),
        MIDDLEWARE=[
            "django.middleware.security.SecurityMiddleware",
            "django.contrib.sessions.middleware.SessionMiddleware",
            "django.middleware.common.CommonMiddleware",
            "django.middleware.csrf.CsrfViewMiddleware",
            "django.contrib.auth.middleware.AuthenticationMiddleware",
            "django.contrib.messages.middleware.MessageMiddleware",
            "django.middleware.clickjacking.XFrameOptionsMiddleware",
        ],
        AUTH_PASSWORD_VALIDATORS=[
            {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
            {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
            {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
            {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
        ],
        REST_FRAMEWORK={"DEFAULT_AUTHENTICATION_CLASSES": ("rest_framework.authentication.TokenAuthentication",)},
        HERBIE_ADMIN={"JS_URL": "js/herbie_core-admin.js", "CSS_URL": "css/herbie_core-admin.css"},
        AUTHENTICATION_BACKENDS=("django.contrib.auth.backends.ModelBackend",),
        ROOT_URLCONF="herbie_core.urls",
        TEMPLATES=[
            {
                "BACKEND": "django.template.backends.django.DjangoTemplates",
                "DIRS": [
                    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "herbie_core/templates")
                ],
                "APP_DIRS": True,
                "OPTIONS": {
                    "context_processors": [
                        "django.template.context_processors.debug",
                        "django.template.context_processors.request",
                        "django.contrib.auth.context_processors.auth",
                        "django.contrib.messages.context_processors.messages",
                    ],
                },
            },
        ],
    )


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        test_path = os.path.dirname(os.path.realpath(__file__))

        fixtures = fnmatch.filter(os.listdir(test_path + "/fixtures"), "*.json")

        for fixture in fixtures:
            call_command("loaddata", test_path + "/fixtures/" + fixture)
