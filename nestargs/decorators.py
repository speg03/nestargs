from .meta import set_metadata


def option(parameter_name, **arg_params):
    def decorator(f):
        set_metadata(f, parameter_name, "arg_params", arg_params)
        return f

    return decorator
