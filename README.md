# nestargs

nestargs is a Python library that defines nested program arguments. It is based on argparse.

[![PyPI](https://img.shields.io/pypi/v/nestargs.svg)](https://pypi.org/project/nestargs/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/nestargs.svg)](https://pypi.org/project/nestargs/)
[![Python Tests](https://github.com/speg03/nestargs/workflows/Python%20Tests/badge.svg)](https://github.com/speg03/nestargs/actions?query=workflow%3A%22Python+Tests%22)
[![codecov](https://codecov.io/gh/speg03/nestargs/branch/master/graph/badge.svg)](https://codecov.io/gh/speg03/nestargs)

Read this in Japanese: [日本語](https://github.com/speg03/nestargs/blob/master/README.ja.md)

## Installation

```
pip install nestargs
```

## Basic usage

Define program arguments in the same way as argparse. A nested structure can be represented by putting a dot in the program argument name.

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
# => NestedNamespace(apple=NestedNamespace(n=2, price=1.5), banana=NestedNamespace(n=3, price=3.5))
```

Let's take out only the program argument apple.

```python
args.apple
# => NestedNamespace(n=2, price=1.5)
```

You can also get each value.

```python
args.apple.price
# => 1.5
```

If you want a dictionary format, you can get it this way.

```python
vars(args.apple)
# => {'n': 2, 'price': 1.5}
```

## Define program arguments from functions

The function `register_arguments` can be used to define program arguments from the parameters any function.

In the following example, program arguments with multiple prefixes are defined as the `n` and `price` parameters of the function `total_price`. At this time, the behavior of the program argument is automatically determined according to the default value of the parameter.

```python
import nestargs


def total_price(n=1, price=1.0):
    return n * price


parser = nestargs.NestedArgumentParser()
parser.register_arguments(total_price, prefix="apple")
parser.register_arguments(total_price, prefix="banana")

args = parser.parse_args(
    ["--apple.n=2", "--apple.price=1.5", "--banana.n=3", "--banana.price=3.5"]
)
# => NestedNamespace(apple=NestedNamespace(n=2, price=1.5), banana=NestedNamespace(n=3, price=3.5))
```

You can call the function with the values obtained from the program arguments as follows:

```python
apple = total_price(**vars(args.apple))
banana = total_price(**vars(args.banana))

print(apple + banana)
# => 13.5
```

### Option decorator

Program argument settings can be added by attaching an `option` decorator to the target function. The settings that can be added are based on `ArgumentParser.add_argument` of `argparse`.

```python
@nestargs.option("n", help="number of ingredients")
@nestargs.option("price", help="unit price of ingredients")
def total_price(n=1, price=1.0):
    return n * price


parser = nestargs.NestedArgumentParser()
parser.register_arguments(total_price, prefix="apple")
```

This code is equivalent to the following code:

```python
def total_price(n=1, price=1.0):
    return n * price


parser = nestargs.NestedArgumentParser()
parser.add_argument("--apple.n", type=int, default=1, help="number of ingredients")
parser.add_argument(
    "--apple.price", type=float, default=1.0, help="unit price of ingredients"
)
```

### Ignores decorator

By attaching an `ignores` decorator to the target function, you can specify parameters that do not register in the program arguments.

```python
@nestargs.ignores("tax", "shipping")
def total_price(n=1, price=1.0, tax=1.0, shipping=0.0):
    return n * price * tax + shipping


parser = nestargs.NestedArgumentParser()
parser.register_arguments(total_price, prefix="apple")

args = parser.parse_args(["--apple.n=2", "--apple.price=1.5"])
# => NestedNamespace(apple=NestedNamespace(n=2, price=1.5))
# Not included tax and shipping parameters

apple = total_price(**vars(args.apple))
# => 3.0
```
