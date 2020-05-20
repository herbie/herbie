from dependency_injector import providers
from herbieapp.initializers.permisson_initializer import PermissionInitializer
from herbieapp.initializers.schema_initializer import SchemaInitializer
import inject


class InitializerInjectConfig:

    def inject_config(binder):
        permission_initializer = providers.Factory(PermissionInitializer)
        schema_initializer = providers.Factory(SchemaInitializer)
        binder.bind(PermissionInitializer, permission_initializer())
        binder.bind(SchemaInitializer, schema_initializer())

