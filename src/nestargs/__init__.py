import importlib.metadata

from .parser import (  # noqa: F401
    ArgumentDefinition,
    NestedArgumentParser,
)

__all__ = [
    "ArgumentDefinition",
    "NestedArgumentParser",
]

__version__ = "0+unknown"
if __package__:
    try:
        __version__ = importlib.metadata.version(__package__)
    except importlib.metadata.PackageNotFoundError:  # pragma: no cover
        pass
