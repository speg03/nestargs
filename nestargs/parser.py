import argparse


class NestedNamespace(argparse.Namespace):
    DELIMITER = '.'

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
            raise ValueError('parent should not be empty: {}'.format(name))
        else:
            super().__setattr__(name, value)


class NestedArgumentParser(argparse.ArgumentParser):
    def parse_known_args(self, args=None, namespace=None):
        if namespace is None:
            namespace = NestedNamespace()
        return super().parse_known_args(args=args, namespace=namespace)
