from herbieapp.initializers.permisson_initializer import PermissionInitializer
from herbieapp.initializers.schema_initializer import SchemaInitializer
from herbieapp.initializers.dependency_providers import InitializerDependencyProvider


class InitializerInjectConfig:
    def inject_config(binder):
        binder.bind(PermissionInitializer, InitializerDependencyProvider.permission_initializer)
        binder.bind(SchemaInitializer, InitializerDependencyProvider.schema_initializer)
