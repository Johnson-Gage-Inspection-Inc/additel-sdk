TYPE_REGISTRY = {
    "System.Double": float
}


def register_type(type_name):
    def wrapper(cls):
        TYPE_REGISTRY[type_name] = cls
        return cls
    return wrapper
