class AbstractInitializer:
    def get_name(self) -> str:
        raise NotImplementedError

    def init(self):
        raise NotImplementedError
