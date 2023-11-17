import argparse

DEFAULT_DELIMITER = "."  # default delimiter for nested namespaces


def create_namespace(delimiter: str):
    class _NestedNamespace(argparse.Namespace):
        def __setattr__(self, name, value):
            if delimiter in name:
                parent, name = name.split(delimiter, maxsplit=1)
            else:
                parent = None

            if parent:
                if not hasattr(self, parent):
                    super().__setattr__(parent, self.__class__())
                setattr(getattr(self, parent), name, value)
            elif parent is not None:
                raise ValueError("parent should not be empty: {}".format(name))
            else:
                super().__setattr__(name, value)

    return _NestedNamespace()


class NestedArgumentParser(argparse.ArgumentParser):
    """ArgumentParser that supports nested namespaces."""

    def __init__(self, delimiter: str = DEFAULT_DELIMITER, **kwargs):
        """Initialize NestedArgumentParser.

        Args:
            delimiter: Delimiter for nested namespaces.
            **kwargs: Keyword arguments for argparse.ArgumentParser.
        """
        self.delimiter = delimiter
        super().__init__(**kwargs)

    def parse_known_args(self, args=None, namespace=None):
        if namespace is None:
            namespace = create_namespace(self.delimiter)
        return super().parse_known_args(args=args, namespace=namespace)
