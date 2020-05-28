import inject
from herbieapp.controllers.inject_config import ControllerInjectConfig
from herbieapp.services.inject_config import ServiceInjectConfig
from herbieapp.initializers.inject_config import InitializerInjectConfig


class InjectConfig:
    def __init__(self):
        inject.configure_once(self.binder_config, bind_in_runtime=False)

    def binder_config(self, binder):
        binder.install(ControllerInjectConfig.inject_config)
        binder.install(ServiceInjectConfig.inject_config)
        binder.install(InitializerInjectConfig.inject_config)



