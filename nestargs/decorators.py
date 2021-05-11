import inspect

from .meta import set_metadata


def option(parameter_name, **arg_params):
    def decorator(f):
        sig = inspect.signature(f)
        if (
            parameter_name not in sig.parameters
            and inspect.Parameter.VAR_KEYWORD
            not in {sig.parameters[k].kind for k in sig.parameters.keys()}
        ):
            raise ValueError(
                "{} doesn't have a parameter: {}".format(f.__name__, parameter_name)
            )
        set_metadata(f, parameter_name, "arg_params", arg_params)
        return f

    return decorator


def ignores(*parameter_names):
    def decorator(f):
        sig = inspect.signature(f)
        for name in parameter_names:
            if name not in sig.parameters:
                raise ValueError(
                    "{} doesn't have a parameter: {}".format(f.__name__, name)
                )
            set_metadata(f, name, "ignore", True)
        return f

    return decorator
