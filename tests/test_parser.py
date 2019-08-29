import pytest

from nestargs import NestedArgumentParser


def foo_function(p1, p2=True, p3=False, p4=1):
    pass


class FooClass:
    def __init__(self, param, *args, **kwargs):
        pass


class TestNestedArgumentParser:
    def test_parse_args(self):
        parser = NestedArgumentParser()
        parser.add_argument("foo.a")
        parser.add_argument("foo.b")
        parser.add_argument("foo.bar.c")

        args = parser.parse_args(["1", "2", "3"])
        assert args.foo.a == "1"
        assert args.foo.b == "2"
        assert args.foo.bar.c == "3"
        assert vars(args.foo).keys() == {"a", "b", "bar"}
        assert vars(args.foo.bar).keys() == {"c"}

    def test_parse_args_with_empty_parent(self):
        parser = NestedArgumentParser()
        parser.add_argument(".empty")

        with pytest.raises(ValueError):
            parser.parse_args([""])

    def test_register_arguments(self):
        parser = NestedArgumentParser()

        actions = parser.register_arguments(foo_function, prefix="foo")
        assert actions.keys() == {"p1", "p2", "p3", "p4"}
        assert actions["p1"].required is True
        assert actions["p2"].default is True
        assert actions["p3"].default is False
        assert actions["p4"].type is int
        assert actions["p4"].default == 1

        args = parser.parse_args(
            ["--foo.p1", "bar", "--foo.no_p2", "--foo.p3", "--foo.p4", "2"]
        )
        assert args.foo.p1 == "bar"
        assert args.foo.p2 is False
        assert args.foo.p3 is True
        assert args.foo.p4 == 2

    def test_register_arguments_with_no_prefixes(self):
        parser = NestedArgumentParser()

        actions = parser.register_arguments(foo_function)
        assert actions.keys() == {"p1", "p2", "p3", "p4"}
        assert actions["p1"].required is True
        assert actions["p2"].default is True
        assert actions["p3"].default is False
        assert actions["p4"].type is int
        assert actions["p4"].default == 1

        args = parser.parse_args(["--p1", "bar", "--no_p2", "--p3", "--p4", "2"])
        assert args.p1 == "bar"
        assert args.p2 is False
        assert args.p3 is True
        assert args.p4 == 2

    def test_register_arguments_from_class(self):
        parser = NestedArgumentParser()

        actions = parser.register_arguments(FooClass, prefix="foo")
        assert actions.keys() == {"param"}
        assert actions["param"].required is True

        args = parser.parse_args(["--foo.param", "bar"])
        assert args.foo.param == "bar"
