import argparse
import inspect


class NestedNamespace(argparse.Namespace):
    DELIMITER = "."

    def __setattr__(self, name, value):
        try:
            parent, name = name.split(self.DELIMITER, maxsplit=1)
        except ValueError:
            parent = None

        if parent:
            if not hasattr(self, parent):
                super().__setattr__(parent, NestedNamespace())
            setattr(getattr(self, parent), name, value)
        elif parent is not None:
            raise ValueError("parent should not be empty: {}".format(name))
        else:
            super().__setattr__(name, value)


class NestedArgumentParser(argparse.ArgumentParser):
    def parse_known_args(self, args=None, namespace=None):
        if namespace is None:
            namespace = NestedNamespace()
        return super().parse_known_args(args=args, namespace=namespace)

    def register_arguments(self, function, prefix=None):
        if inspect.isclass(function):
            sig = inspect.signature(function.__init__)
        else:
            sig = inspect.signature(function)

        if prefix:
            argument_prefix = prefix + "."
            target = self.add_argument_group(prefix)
        else:
            argument_prefix = ""
            target = self

        actions = {}
        for parameter in sig.parameters.values():
            if (
                parameter.name == "self"
                or parameter.name == "cls"
                or parameter.kind is inspect.Parameter.VAR_POSITIONAL
                or parameter.kind is inspect.Parameter.VAR_KEYWORD
            ):
                continue  # pragma: no cover

            name = parameter.name
            options = {}
            if parameter.default is inspect.Parameter.empty:
                options["required"] = True
            else:
                if parameter.default is True:
                    options["action"] = "store_false"
                    options["dest"] = argument_prefix + name
                    name = "no_" + name
                elif parameter.default is False:
                    options["action"] = "store_true"
                elif type(parameter.default) in {int, float}:
                    options["type"] = type(parameter.default)

                options["default"] = parameter.default

            argument_name = "--" + argument_prefix + name
            actions[parameter.name] = target.add_argument(argument_name, **options)

        return actions
