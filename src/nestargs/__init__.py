import importlib.metadata

from .parser import ArgumentDefinition, ArgumentTypeError, NestedArgumentParser

__all__ = [
    "ArgumentDefinition",
    "ArgumentTypeError",
    "NestedArgumentParser",
]

__version__ = "0+unknown"
if __package__:
    try:
        __version__ = importlib.metadata.version(__package__)
    except importlib.metadata.PackageNotFoundError:  # pragma: no cover
        pass
