import inject
from herbieapp.controllers.inject_config import ControllerInjectConfig
from herbieapp.services.inject_config import ServiceInjectConfig
from herbieapp.initializers.inject_config import InitializerInjectConfig


class InjectConfig:

    def inject_config(binder):
        binder.install(ControllerInjectConfig.inject_config)
        binder.install(ServiceInjectConfig.inject_config)
        binder.install(InitializerInjectConfig.inject_config)

    inject.configure_once(inject_config)
