# connection/base.py

class Connection:
    registry = {}

    def __init_subclass__(cls, **kwargs):
        """Automatically register subclasses using their `type` attribute."""
        super().__init_subclass__(**kwargs)
        if hasattr(cls, "type"):
            Connection.registry[cls.type] = cls

    def __new__(cls, parent, connection_type, **kwargs):
        if cls is Connection:
            subclass = cls.registry.get(connection_type)
            if not subclass:
                raise ValueError(f"Unsupported connection type: {connection_type}")
            instance = super().__new__(subclass)
            instance.__init__(parent, **kwargs)
            return instance
        return super().__new__(cls)

    def __init__(self, parent, **kwargs):
        if type(self) is not Connection:
            return
        self.parent = parent
        # Store each remaining kwarg as an attribute
        for key, value in kwargs.items():
            setattr(self, key, value)

    def connect(self):
        raise NotImplementedError

    def disconnect(self):
        raise NotImplementedError

    @classmethod
    def available_types(cls):
        return list(cls.registry.keys())
