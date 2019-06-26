# nestargs

nestargs is a Python library that defines nested program arguments. It is based on argparse.

[![PyPI](https://img.shields.io/pypi/v/nestargs.svg)](https://pypi.org/project/nestargs/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/nestargs.svg)](https://pypi.org/project/nestargs/)
[![Build Status](https://travis-ci.com/speg03/nestargs.svg?branch=master)](https://travis-ci.com/speg03/nestargs)
[![codecov](https://codecov.io/gh/speg03/nestargs/branch/master/graph/badge.svg)](https://codecov.io/gh/speg03/nestargs)

Read this in Japanese: [日本語](README.ja.md)

## Installation

```
pip install nestargs
```

## Usage

### Basic

Define program arguments in the same way as argparse. A nested structure can be represented by putting a dot in the program argument name.

```python
import nestargs

parser = nestargs.NestedArgumentParser()

parser.add_argument('--apple.n', type=int)
parser.add_argument('--apple.price', type=float)

parser.add_argument('--banana.n', type=int)
parser.add_argument('--banana.price', type=float)

args = parser.parse_args('--apple.n=2 --apple.price=1.5 --banana.n=3 --banana.price=3.5'.split())
# NestedNamespace(apple=NestedNamespace(n=2, price=1.5), banana=NestedNamespace(n=3, price=3.5))
```

Let's take out only the program argument apple.

```python
args.apple
# NestedNamespace(n=2, price=1.5)
```

You can also get each value.

```python
args.apple.price
# 1.5
```

If you want a dictionary format, you can get it this way.

```python
vars(args.apple)
# {'n': 2, 'price': 1.5}
```
