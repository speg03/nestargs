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

## 使い方

### 基本

argparseと同じ方法でプログラム引数を定義します。プログラム引数の名前にドットを入れることで、入れ子構造を表すことができます。

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

プログラム引数appleだけを取り出してみましょう。

```python
args.apple
# NestedNamespace(n=2, price=1.5)
```

それぞれの値も取り出すことができます。

```python
args.apple.price
# 1.5
```

dict形式がよければこうして取り出すことができます。

```python
vars(args.apple)
# {'n': 2, 'price': 1.5}
```
