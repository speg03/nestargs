import inspect

from .meta import set_metadata


def option(parameter_name, **arg_params):
    def decorator(f):
        sig = inspect.signature(f)
        if parameter_name not in sig.parameters:
            raise ValueError(
                "{} doesn't have a parameter: {}".format(f.__name__, parameter_name)
            )
        set_metadata(f, parameter_name, "arg_params", arg_params)
        return f

    return decorator
