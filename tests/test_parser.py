import pytest

from nestargs import NestedArgumentParser


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
