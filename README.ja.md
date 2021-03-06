# nestargs

nestargsは入れ子構造になったプログラム引数を定義するPythonライブラリです。argparseをもとにしています。

[![PyPI](https://img.shields.io/pypi/v/nestargs.svg)](https://pypi.org/project/nestargs/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/nestargs.svg)](https://pypi.org/project/nestargs/)
[![Python Tests](https://github.com/speg03/nestargs/workflows/Python%20Tests/badge.svg)](https://github.com/speg03/nestargs/actions?query=workflow%3A%22Python+Tests%22)
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

### option デコレータ

対象の関数に `option` デコレータを付与することで、プログラム引数の設定を追加することができます。追加できる設定は `argparse` の `ArgumentParser.add_argument` に基づきます。

```python
@nestargs.option("n", help="number of ingredients")
@nestargs.option("price", help="unit price of ingredients")
def total_price(n=1, price=1.0):
    return n * price


parser = nestargs.NestedArgumentParser()
parser.register_arguments(total_price, prefix="apple")
```

このコードは次のコードと等価です。

```python
def total_price(n=1, price=1.0):
    return n * price


parser = nestargs.NestedArgumentParser()
parser.add_argument("--apple.n", type=int, default=1, help="number of ingredients")
parser.add_argument(
    "--apple.price", type=float, default=1.0, help="unit price of ingredients"
)
```

### ignores デコレータ

対象の関数に `ignores` デコレータを付与することで、プログラム引数に登録しないパラメータを指定することができます。

```python
@nestargs.ignores("tax", "shipping")
def total_price(n=1, price=1.0, tax=1.0, shipping=0.0):
    return n * price * tax + shipping


parser = nestargs.NestedArgumentParser()
parser.register_arguments(total_price, prefix="apple")

args = parser.parse_args(["--apple.n=2", "--apple.price=1.5"])
# => NestedNamespace(apple=NestedNamespace(n=2, price=1.5))
# taxとshippingパラメータが含まれていません

apple = total_price(**vars(args.apple))
# => 3.0
```
