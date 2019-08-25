# nestargs

nestargsは入れ子構造になったプログラム引数を定義するPythonライブラリです。argparseをもとにしています。

[![PyPI](https://img.shields.io/pypi/v/nestargs.svg)](https://pypi.org/project/nestargs/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/nestargs.svg)](https://pypi.org/project/nestargs/)
[![Build Status](https://travis-ci.com/speg03/nestargs.svg?branch=master)](https://travis-ci.com/speg03/nestargs)
[![codecov](https://codecov.io/gh/speg03/nestargs/branch/master/graph/badge.svg)](https://codecov.io/gh/speg03/nestargs)

## インストール

```
pip install nestargs
```

## 基本的な使い方

argparseと同じ方法でプログラム引数を定義します。プログラム引数の名前にドットを入れることで、入れ子構造を表すことができます。

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

プログラム引数appleだけを取り出してみましょう。

```python
args.apple
# => NestedNamespace(n=2, price=1.5)
```

それぞれの値も取り出すことができます。

```python
args.apple.price
# => 1.5
```

dict形式がよければこうして取り出すことができます。

```python
vars(args.apple)
# => {'n': 2, 'price': 1.5}
```

## 関数からプログラム引数を定義

`register_arguments` という関数を使って、任意の関数の引数からプログラム引数を定義することができます。

次の例では、 `total_price` という関数の `n`, `price` という引数について、prefixを変えながらプログラム引数を定義しています。このとき、引数のデフォルト値によってプログラム引数の挙動を自動的に設定します。

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

プログラム引数から得られた値を使って、次のように関数を呼び出すことができます。

```python
apple = total_price(**vars(args.apple))
banana = total_price(**vars(args.banana))

print(apple + banana)
# => 13.5
```
