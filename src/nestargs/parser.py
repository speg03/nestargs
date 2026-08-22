import argparse
from dataclasses import dataclass
from typing import Any

DEFAULT_DELIMITER = "."  # default delimiter for nested namespaces
_MISSING = object()


@dataclass(frozen=True)
class ArgumentDefinition:
    """Definition for a parsed command line argument."""

    name: str
    nargs: int | str | None = None
    default: Any = _MISSING
    type: Any = None
    dest: str | None = None


def _normalize_option_key(name: str) -> str:
    normalized = name.strip("_")
    normalized = normalized.replace("_", "-")
    return normalized


def _build_option_name(
    path: tuple[str, ...], delimiter: str = DEFAULT_DELIMITER
) -> str:
    normalized = delimiter.join(_normalize_option_key(str(part)) for part in path)
    return f"--{normalized}"


def _parse_bool(value: str) -> bool:
    normalized = value.lower()
    if normalized == "true":
        return True
    if normalized == "false":
        return False
    raise argparse.ArgumentTypeError("expected 'true' or 'false'")


def _infer_argument_type(value: Any):
    if value is None:
        return None
    if isinstance(value, bool):
        return _parse_bool
    if isinstance(value, int):
        return int
    if isinstance(value, float):
        return float
    if isinstance(value, str):
        return str
    return str


def create_argument_definitions_from_dict(
    values: dict[str, Any],
    *,
    max_depth: int = 1,
    delimiter: str = DEFAULT_DELIMITER,
    prefix: tuple[str, ...] = (),
):
    """Create ArgumentDefinition objects from a nested dictionary.

    Arguments deeper than max_depth are treated as a single string-valued CLI argument
    whose value is the literal string representation of the nested dict.
    """
    if not isinstance(values, dict):
        raise TypeError(f"values must be dict, got {type(values).__name__}")
    if max_depth < 0:
        raise ValueError("max_depth must be >= 0")

    definitions: list[ArgumentDefinition] = []

    def _walk(current: dict[str, Any], depth: int, path: tuple[str, ...]):
        for key, value in current.items():
            current_path = (*path, str(key))
            full_dest = delimiter.join(current_path)
            option_name = _build_option_name(current_path, delimiter=delimiter)

            if isinstance(value, dict):
                if depth < max_depth:
                    _walk(value, depth + 1, current_path)
                else:
                    definitions.append(
                        ArgumentDefinition(
                            name=option_name,
                            default=str(value),
                            type=str,
                            dest=full_dest,
                        )
                    )
                continue

            definitions.append(
                ArgumentDefinition(
                    name=option_name,
                    default=value,
                    type=_infer_argument_type(value),
                    dest=full_dest,
                )
            )

    _walk(values, 0, prefix)
    return definitions


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

    def add_arguments(self, *definitions):
        """Register multiple arguments from ArgumentDefinition objects."""
        if len(definitions) == 1 and isinstance(definitions[0], (list, tuple)):
            definitions = tuple(definitions[0])

        for definition in definitions:
            if not isinstance(definition, ArgumentDefinition):
                raise TypeError(
                    "Each item passed to add_arguments must be an ArgumentDefinition, "
                    f"got {type(definition).__name__}"
                )

            kwargs = {}
            if definition.nargs is not None:
                kwargs["nargs"] = definition.nargs
            if definition.default is not _MISSING:
                kwargs["default"] = definition.default
            if definition.type is not None:
                kwargs["type"] = definition.type
            if definition.dest is not None:
                kwargs["dest"] = definition.dest

            self.add_argument(definition.name, **kwargs)

    def add_arguments_from_dict(
        self,
        values: dict[str, Any],
        *,
        max_depth: int = 1,
        delimiter: str | None = None,
    ):
        """Register arguments created from a nested dictionary."""
        if delimiter is None:
            delimiter = self.delimiter

        definitions = create_argument_definitions_from_dict(
            values,
            max_depth=max_depth,
            delimiter=delimiter,
        )
        self.add_arguments(definitions)

    def parse_known_args(self, args=None, namespace=None):
        if namespace is None:
            namespace = create_namespace(self.delimiter)
        return super().parse_known_args(args=args, namespace=namespace)
