ATTRIBUTE = "__nestargs__"


def set_metadata(function, parameter_name, key, value):
    if not hasattr(function, ATTRIBUTE):
        setattr(function, ATTRIBUTE, {})
    attr = getattr(function, ATTRIBUTE)
    attr.setdefault(parameter_name, {})[key] = value


def get_metadata(function, parameter_name, key):
    if hasattr(function, ATTRIBUTE):
        return getattr(function, ATTRIBUTE).get(parameter_name, {}).get(key)
    return None
