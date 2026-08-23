# User guide

## Basic usage

When defining command-line arguments, use a period (`.`) as the delimiter to represent a variable hierarchy. The following example defines `n` and `price` arguments under both the `apple` and `banana` hierarchies independently.

```python
import nestargs

parser = nestargs.NestedArgumentParser()

parser.add_argument("--apple.n", type=int)
parser.add_argument("--apple.price", type=float)

parser.add_argument("--banana.n", type=int)
parser.add_argument("--banana.price", type=float)

args = parser.parse_args(
    ["--apple.n=2", "--apple.price=1.5", "--banana.n=3", "--banana.price=3.5"]
)
# => _NestedNamespace(apple=_NestedNamespace(n=2, price=1.5), banana=_NestedNamespace(n=3, price=3.5))
```

Arguments obtained by parsing command-line inputs can be accessed through their hierarchical structure.

```python
args.apple
# => _NestedNamespace(n=2, price=1.5)
```

You can also refer directly to variables nested deeper in the hierarchy.

```python
args.apple.price
# => 1.5
```

When referring to a level in the hierarchy, you can use `vars` to create a dictionary.

```python
vars(args.apple)
# => {'n': 2, 'price': 1.5}
```

## Defining arguments from a dictionary

Use `add_arguments_from_dict` to define arguments from a dictionary of default
values. Keys become long option names, and nested dictionaries become nested
namespaces. Scalar values infer their command-line type from the default value.

```python
import nestargs

parser = nestargs.NestedArgumentParser()
parser.add_arguments_from_dict(
    {
        "server": {
            "host": "localhost",
            "port": 8080,
        },
        "debug": False,
    }
)

args = parser.parse_args(["--server.host", "example.com", "--debug", "true"])

args.server.host
# => 'example.com'
args.server.port
# => 8080
args.debug
# => True
```

The inferred scalar types are `bool`, `int`, `float`, and `str`. Boolean values
must be supplied as `true` or `false`.

Dictionary keys are converted to long option names as follows:

- Every option name starts with `--`.
- Leading and trailing underscores are removed from the option name.
- Remaining underscores are replaced with hyphens.
- Nested key separators use the parser's delimiter.

For example, `_first_name_` under `user_profile` becomes the option
`--user-profile.first-name`, while the parsed value is accessible as
`args.user_profile._first_name_`.

### JSON values for lists and deep dictionaries

Lists are supplied as one JSON array argument. Dictionaries deeper than
`max_depth` are supplied as one JSON object argument. Their default values remain
structured Python values when the option is omitted.

```python
import nestargs

parser = nestargs.NestedArgumentParser()
parser.add_arguments_from_dict(
    {
        "tags": ["stable"],
        "service": {
            "connection": {
                "timeout": 30,
            },
        },
    },
    max_depth=1,
)

args = parser.parse_args(
    [
        "--tags",
        '["stable", "fast"]',
        "--service.connection",
        '{"timeout": 60}',
    ]
)

args.tags
# => ['stable', 'fast']
args.service.connection
# => {'timeout': 60}
```

## Using a different namespace delimiter

The default namespace delimiter is a period (`.`), but you can use any other character. To do so, specify the delimiter as an argument to the `NestedArgumentParser` constructor.

```python
import nestargs

parser = nestargs.NestedArgumentParser(delimiter="/")
parser.add_argument("--apple/n", type=int)

args = parser.parse_args(["--apple/n=1"])
# => _NestedNamespace(apple=_NestedNamespace(n=1))
```

However, use the period (`.`) delimiter when accessing variables, regardless of the argument delimiter.

```python
args.apple.n
# => 1
```
