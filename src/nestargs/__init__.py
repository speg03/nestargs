import importlib.metadata

from .parser import (  # noqa: F401
    ArgumentDefinition,
    NestedArgumentParser,
    create_argument_definitions_from_dict,
)

__all__ = [
    "ArgumentDefinition",
    "NestedArgumentParser",
    "create_argument_definitions_from_dict",
]

__version__ = "0+unknown"
if __package__:
    try:
        __version__ = importlib.metadata.version(__package__)
    except importlib.metadata.PackageNotFoundError:  # pragma: no cover
        pass
