import pytest

from nestargs import NestedArgumentParser


class TestNestedArgumentParser:
    def test_parse_args(self):
        parser = NestedArgumentParser()
        parser.add_argument("foo.a")
        parser.add_argument("foo.b")

        args = parser.parse_args(["1", "2"])
        assert args.foo.a == "1"
        assert args.foo.b == "2"
        assert vars(args.foo) == {"a": "1", "b": "2"}

    def test_parse_args_with_empty_parent(self):
        parser = NestedArgumentParser()
        parser.add_argument(".empty")

        with pytest.raises(ValueError):
            parser.parse_args([""])
