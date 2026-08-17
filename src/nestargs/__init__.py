import importlib.metadata

from .parser import NestedArgumentParser  # noqa: F401

__version__ = "0+unknown"
if __package__:
    try:
        __version__ = importlib.metadata.version(__package__)
    except importlib.metadata.PackageNotFoundError:  # pragma: no cover
        pass
