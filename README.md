# nestargs

*nestargs* is a Python library that treats command line arguments as a hierarchical structure. The functionality for interpreting command line arguments is the same as argparse.

[![PyPI](https://img.shields.io/pypi/v/nestargs)](https://pypi.org/project/nestargs/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/nestargs)](https://pypi.org/project/nestargs/)
[![Python Tests](https://github.com/speg03/nestargs/actions/workflows/python-tests.yml/badge.svg)](https://github.com/speg03/nestargs/actions/workflows/python-tests.yml)
[![codecov](https://codecov.io/gh/speg03/nestargs/graph/badge.svg?token=mOzO3kbpDl)](https://codecov.io/gh/speg03/nestargs)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/speg03/nestargs/main.svg)](https://results.pre-commit.ci/latest/github/speg03/nestargs/main)

## Installation

```
pip install nestargs
```

## Basic usage

When defining command line arguments, use "." as the delimiter. to represent a variable hierarchy. The following code example defines an `n` and `price` variable in the `apple` hierarchy and another separate `n` and `price` variable in the `banana` hierarchy.

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

Variables obtained by parsing command line arguments can be referenced by hierarchy.

```python
args.apple
# => _NestedNamespace(n=2, price=1.5)
```

Of course, you can also refer directly to variables lower down in the hierarchy.

```python
args.apple.price
# => 1.5
```

When referring to each level of hierarchy, you can use `vars` to create a dictionary format.

```python
vars(args.apple)
# => {'n': 2, 'price': 1.5}
```

## Use a different delimiter for namespace

The default namespace delimiter is "." but can be any other character. In that case, specify the delimiter in the `NestedArgumentParser` constructor argument.

```python
import nestargs

parser = nestargs.NestedArgumentParser(delimiter="/")
parser.add_argument("--apple/n", type=int)

args = parser.parse_args(["--apple/n=1"])
# => _NestedNamespace(apple=_NestedNamespace(n=1))
```

However, references to variables must be separated by "." delimiter when referring to variables.

```python
args.apple.n
# => 1
```
