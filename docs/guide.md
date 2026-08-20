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

Arguments obtained by parsing command-line arguments can be accessed through their hierarchical structure.

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
